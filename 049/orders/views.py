from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from .models import Customer, WholesaleOrder, WholesaleOrderItem, Settlement
from .serializers import CustomerSerializer, WholesaleOrderSerializer, WholesaleOrderItemSerializer, SettlementSerializer
from inventory.services import InventoryService
from accounts.permissions import CustomerManagePermission, OrderManagePermission, SettlementManagePermission


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), CustomerManagePermission()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        is_active = self.request.query_params.get('is_active')
        
        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(contact_person__icontains=name))
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        self.validate_customer_data(serializer.validated_data)
        serializer.save()

    def perform_update(self, serializer):
        self.validate_customer_data(serializer.validated_data)
        serializer.save()

    def validate_customer_data(self, data):
        if not data.get('customer_code'):
            raise ValidationError({'customer_code': ['客户编号为必填项']})
        if not data.get('name'):
            raise ValidationError({'name': ['客户名称为必填项']})


class WholesaleOrderViewSet(viewsets.ModelViewSet):
    queryset = WholesaleOrder.objects.all()
    serializer_class = WholesaleOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), OrderManagePermission()]
        if self.action in ['start_delivery', 'complete', 'cancel']:
            return [IsAuthenticated(), OrderManagePermission()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        order_status = self.request.query_params.get('status')
        customer_id = self.request.query_params.get('customer')
        order_no = self.request.query_params.get('order_no')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if order_status:
            queryset = queryset.filter(status=order_status)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if order_no:
            queryset = queryset.filter(order_no__icontains=order_no)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        self.validate_order_data(serializer.validated_data)
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.status != 'pending':
            raise ValidationError({'error': ['只有待出库的订单才能修改']})
        self.validate_order_data(serializer.validated_data)
        serializer.save()

    def validate_order_data(self, data):
        if not data.get('customer'):
            raise ValidationError({'customer': ['客户为必填项']})

    @action(detail=True, methods=['post'])
    def start_delivery(self, request, pk=None):
        wholesale_order = self.get_object()
        if wholesale_order.status != 'pending':
            return Response(
                {'error': '只有待出库的订单才能开始配送'},
                status=status.HTTP_400_BAD_REQUEST
            )

        items = wholesale_order.items.all()
        if not items.exists():
            return Response(
                {'error': '订单明细为空，无法出库'},
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in items:
            if item.quantity <= 0:
                return Response(
                    {'error': f'商品 {item.product.name} 出库数量必须大于0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if item.unit_price < 0:
                return Response(
                    {'error': f'商品 {item.product.name} 单价不能为负数'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        alert_messages = []
        try:
            with transaction.atomic():
                for item in items:
                    result = InventoryService.stock_out(
                        product=item.product,
                        quantity=item.quantity,
                        related_order_no=wholesale_order.order_no,
                        remark=f'批发订单出库'
                    )
                
                InventoryService.check_stock_alert(item.product)

                for item in items:
                    alert_result = InventoryService.check_stock_alert(item.product)
                    if alert_result['has_alert']:
                        alert_messages.append(alert_result['message'])

                wholesale_order.status = 'delivering'
                wholesale_order.save()

            response_data = {'message': '开始配送'}
            if alert_messages:
                response_data['warnings'] = alert_messages
            return Response(response_data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        wholesale_order = self.get_object()
        if wholesale_order.status != 'delivering':
            return Response(
                {'error': '只有配送中的订单才能完成'},
                status=status.HTTP_400_BAD_REQUEST
            )
        wholesale_order.status = 'completed'
        wholesale_order.save()

        Settlement.objects.get_or_create(
            wholesale_order=wholesale_order,
            defaults={
                'total_amount': wholesale_order.total_amount,
                'status': 'unpaid'
            }
        )

        return Response({'message': '订单已完成'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        wholesale_order = self.get_object()
        if wholesale_order.status not in ['pending', 'delivering']:
            return Response(
                {'error': '该状态的订单不能作废'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if wholesale_order.status == 'delivering':
            try:
                with transaction.atomic():
                    for item in wholesale_order.items.all():
                        InventoryService.stock_in(
                            product=item.product,
                            quantity=item.quantity,
                            related_order_no=wholesale_order.order_no,
                            remark=f'订单作废退回'
                        )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        wholesale_order.status = 'cancelled'
        wholesale_order.save()
        return Response({'message': '订单已作废'})


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'confirm_payment']:
            return [IsAuthenticated(), SettlementManagePermission()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        settlement_status = self.request.query_params.get('status')
        settlement_no = self.request.query_params.get('settlement_no')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if settlement_status:
            queryset = queryset.filter(status=settlement_status)
        if settlement_no:
            queryset = queryset.filter(settlement_no__icontains=settlement_no)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        settlement = self.get_object()
        if settlement.status != 'unpaid':
            return Response(
                {'error': '该结算单已结算'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment_method = request.data.get('payment_method', '')
        if not payment_method:
            return Response(
                {'error': '支付方式为必填项'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        settlement.status = 'paid'
        settlement.payment_method = payment_method
        settlement.settled_at = timezone.now()
        settlement.save()
        
        return Response({'message': '结算成功'})
