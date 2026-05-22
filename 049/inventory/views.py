from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from .models import Inventory, StockRecord, StockAlert
from .serializers import InventorySerializer, StockRecordSerializer, StockAlertSerializer


class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_name = self.request.query_params.get('product_name')
        product_id = self.request.query_params.get('product')
        stock_status = self.request.query_params.get('stock_status')
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if product_name:
            queryset = queryset.filter(
                Q(product__name__icontains=product_name) | 
                Q(product__product_code__icontains=product_name)
            )
        if stock_status:
            product_ids = []
            for inv in queryset:
                if stock_status == 'low' and inv.is_low_stock:
                    product_ids.append(inv.product_id)
                elif stock_status == 'out' and inv.quantity <= 0:
                    product_ids.append(inv.product_id)
                elif stock_status == 'normal' and not inv.is_low_stock and inv.quantity > 0:
                    product_ids.append(inv.product_id)
            queryset = queryset.filter(product_id__in=product_ids)
        
        return queryset.order_by('-last_updated')

    @action(detail=False, methods=['get'])
    def low_stock_alerts(self, request):
        low_stock_items = []
        for inventory in Inventory.objects.all():
            if inventory.is_low_stock:
                low_stock_items.append(inventory)
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = Inventory.objects.count()
        low_stock_count = sum(1 for inv in Inventory.objects.all() if inv.is_low_stock)
        out_stock_count = sum(1 for inv in Inventory.objects.all() if inv.quantity <= 0)
        return Response({
            'total_products': total,
            'low_stock_count': low_stock_count,
            'out_stock_count': out_stock_count,
            'normal_stock_count': total - low_stock_count - out_stock_count
        })


class StockRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockRecord.objects.all()
    serializer_class = StockRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product')
        record_type = self.request.query_params.get('type')
        related_order_no = self.request.query_params.get('order_no')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if record_type:
            queryset = queryset.filter(record_type=record_type)
        if related_order_no:
            queryset = queryset.filter(related_order_no__icontains=related_order_no)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')


class StockAlertViewSet(viewsets.ModelViewSet):
    queryset = StockAlert.objects.all()
    serializer_class = StockAlertSerializer
    http_method_names = ['get', 'put', 'patch', 'head', 'options']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_handled = self.request.query_params.get('is_handled')
        alert_type = self.request.query_params.get('alert_type')
        product_name = self.request.query_params.get('product_name')
        
        if is_handled is not None:
            queryset = queryset.filter(is_handled=(is_handled.lower() == 'true'))
        if alert_type:
            queryset = queryset.filter(alert_type=alert_type)
        if product_name:
            queryset = queryset.filter(
                Q(product__name__icontains=product_name) |
                Q(product__product_code__icontains=product_name)
            )
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def handle_alert(self, request, pk=None):
        alert = self.get_object()
        if alert.is_handled:
            raise ValidationError({'error': ['该预警已处理']})
        alert.is_handled = True
        alert.handled_at = timezone.now()
        alert.save()
        return Response({'message': '预警已处理'})

    @action(detail=False, methods=['post'])
    def handle_all(self, request):
        count = StockAlert.objects.filter(is_handled=False).update(
            is_handled=True,
            handled_at=timezone.now()
        )
        return Response({'message': f'已处理 {count} 条预警'})
