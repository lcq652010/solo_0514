from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Customer, Device, RepairOrder, Notification, ArchivedOrder
from .serializers import (
    CustomerSerializer, DeviceSerializer, RepairOrderSerializer,
    NotificationSerializer, ArchivedOrderSerializer, RepairOrderListSerializer,
    UserSerializer
)
from .filters import RepairOrderFilter, CustomerFilter, DeviceFilter, NotificationFilter
from .permissions import IsAdmin, IsAdminOrReception, RepairOrderPermission
from .pagination import CustomPageNumberPagination, SmallResultsSetPagination


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter
    permission_classes = [IsAdminOrReception]
    pagination_class = SmallResultsSetPagination
    search_fields = ['name', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filterset_class = DeviceFilter
    permission_classes = [IsAdminOrReception]
    pagination_class = SmallResultsSetPagination
    search_fields = ['brand', 'model', 'customer__name']
    ordering_fields = ['brand', 'model', 'created_at']
    ordering = ['-created_at']


class RepairOrderViewSet(viewsets.ModelViewSet):
    queryset = RepairOrder.objects.all()
    filterset_class = RepairOrderFilter
    permission_classes = [RepairOrderPermission]
    pagination_class = CustomPageNumberPagination
    search_fields = ['order_number', 'customer__name', 'device__brand', 'device__model']
    ordering_fields = ['created_at', 'updated_at', 'status', 'actual_cost']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RepairOrderListSerializer
        return RepairOrderSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.profile.role == 'engineer':
            queryset = queryset.filter(assigned_to=user)
        return queryset
    
    def perform_create(self, serializer):
        last_order = RepairOrder.objects.order_by('-id').first()
        order_number = f'WO{timezone.now().strftime("%Y%m%d")}{(last_order.id + 1) if last_order else 1:04d}'
        serializer.save(order_number=order_number, created_by=self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if 'assigned_to' in serializer.validated_data and serializer.validated_data['assigned_to']:
            Notification.create_order_assigned_notification(instance, serializer.validated_data['assigned_to'])
    
    @action(detail=True, methods=['post'])
    def pick_up(self, request, pk=None):
        repair_order = self.get_object()
        if repair_order.status != 'completed':
            return Response({'error': '只有已完成的工单才能取机'}, status=status.HTTP_400_BAD_REQUEST)
        
        repair_order.status = 'picked_up'
        repair_order.picked_up_at = timezone.now()
        repair_order.save()
        
        users = User.objects.filter(profile__role__in=['admin', 'reception'])
        for user in users:
            Notification.objects.create(
                user=user,
                notification_type='status_changed',
                title=f'工单{repair_order.order_number}已取机',
                content=f'客户{repair_order.customer.name}的设备已取机，请确认是否需要归档。',
                related_order=repair_order
            )
        
        auto_archive = request.data.get('auto_archive', False)
        if auto_archive:
            ArchivedOrder.archive_from_repair_order(repair_order, request.user)
            return Response({'status': '取机成功并已自动归档', 'archived': True})
        
        return Response({'status': '取机成功', 'archived': False})
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        repair_order = self.get_object()
        if repair_order.status != 'picked_up':
            return Response({'error': '只有已取机的工单才能归档'}, status=status.HTTP_400_BAD_REQUEST)
        
        ArchivedOrder.archive_from_repair_order(repair_order, request.user)
        
        users = User.objects.filter(profile__role='admin')
        for user in users:
            Notification.objects.create(
                user=user,
                notification_type='system',
                title=f'工单{repair_order.order_number}已归档',
                content=f'工单{repair_order.order_number}已由{request.user.username}归档。',
                related_order=repair_order
            )
        
        return Response({'status': '归档成功', 'order_number': repair_order.order_number})
    
    @action(detail=False, methods=['post'])
    def auto_archive(self, request):
        if request.user.profile.role != 'admin':
            return Response({'error': '只有管理员可以执行批量归档'}, status=status.HTTP_403_FORBIDDEN)
        
        days = int(request.data.get('days', 7))
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        picked_up_orders = RepairOrder.objects.filter(
            status='picked_up',
            picked_up_at__lte=cutoff_date
        )
        
        count = 0
        archived_numbers = []
        for order in picked_up_orders:
            ArchivedOrder.archive_from_repair_order(order, request.user)
            archived_numbers.append(order.order_number)
            count += 1
        
        if count > 0:
            User.objects.filter(profile__role='admin').exclude(id=request.user.id).update()
            for user in User.objects.filter(profile__role='admin').exclude(id=request.user.id):
                Notification.objects.create(
                    user=user,
                    notification_type='system',
                    title=f'批量归档完成',
                    content=f'{request.user.username}已自动归档{count}个超过{days}天的工单。',
                )
        
        return Response({
            'status': f'成功归档{count}个工单',
            'archived_count': count,
            'archived_orders': archived_numbers,
            'days': days
        })
    
    @action(detail=False, methods=['get'])
    def archive_candidates(self, request):
        if request.user.profile.role not in ['admin', 'reception']:
            return Response({'error': '无权限查看'}, status=status.HTTP_403_FORBIDDEN)
        
        days = int(request.query_params.get('days', 7))
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        candidates = RepairOrder.objects.filter(
            status='picked_up',
            picked_up_at__lte=cutoff_date
        ).order_by('picked_up_at')
        
        serializer = self.get_serializer(candidates, many=True)
        return Response({
            'count': candidates.count(),
            'days': days,
            'candidates': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        repair_order = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = [choice[0] for choice in RepairOrder.STATUS_CHOICES]
        
        if new_status not in valid_statuses:
            return Response({'error': '无效的状态'}, status=status.HTTP_400_BAD_REQUEST)
        
        repair_order.status = new_status
        repair_order.save()
        return Response({'status': '状态更新成功', 'new_status': new_status})
    
    @action(detail=False, methods=['get'])
    def engineer_workload(self, request):
        engineers = User.objects.filter(profile__role='engineer')
        workload_data = []
        for engineer in engineers:
            active_count = RepairOrder.objects.filter(
                assigned_to=engineer,
                status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
            ).count()
            workload_data.append({
                'engineer_id': engineer.id,
                'engineer_name': engineer.username,
                'active_orders': active_count,
                'max_orders': 10,
                'available_slots': max(0, 10 - active_count)
            })
        return Response(workload_data)
    
    @action(detail=True, methods=['get'])
    def check_assignment_conflict(self, request, pk=None):
        repair_order = self.get_object()
        engineer_id = request.query_params.get('engineer_id')
        
        if not engineer_id:
            return Response({'error': '必须提供工程师ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            engineer = User.objects.get(id=engineer_id)
            if engineer.profile.role != 'engineer':
                return Response({'conflict': True, 'message': '该用户不是工程师角色'})
        except User.DoesNotExist:
            return Response({'error': '工程师不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        active_count = RepairOrder.objects.filter(
            ~Q(id=repair_order.id),
            assigned_to=engineer,
            status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
        ).count()
        
        has_conflict = active_count >= 10
        return Response({
            'conflict': has_conflict,
            'active_orders': active_count,
            'max_orders': 10,
            'available_slots': max(0, 10 - active_count),
            'message': '该工程师派单数量已达上限' if has_conflict else '可以分配'
        })


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilter
    pagination_class = SmallResultsSetPagination
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'is_read']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': '已标记为已读', 'id': notification.id})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        updated_count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'status': '全部标记为已读', 'updated_count': updated_count})
    
    @action(detail=False, methods=['post'])
    def mark_selected_read(self, request):
        notification_ids = request.data.get('ids', [])
        if not notification_ids:
            return Response({'error': '请选择要标记的通知'}, status=status.HTTP_400_BAD_REQUEST)
        updated_count = self.get_queryset().filter(id__in=notification_ids, is_read=False).update(is_read=True)
        return Response({'status': '已标记选中通知为已读', 'updated_count': updated_count})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        limit = int(request.query_params.get('limit', 10))
        notifications = self.get_queryset().order_by('-created_at')[:limit]
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)


class ArchivedOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchivedOrder.objects.all()
    serializer_class = ArchivedOrderSerializer
    permission_classes = [IsAdmin]
    search_fields = ['order_number', 'customer_name', 'device_info']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    
    @action(detail=False, methods=['get'])
    def engineers(self, request):
        engineers = User.objects.filter(profile__role='engineer')
        serializer = self.get_serializer(engineers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    stats = {
        'total_orders': RepairOrder.objects.count(),
        'pending_orders': RepairOrder.objects.filter(status='pending').count(),
        'repairing_orders': RepairOrder.objects.filter(status='repairing').count(),
        'completed_orders': RepairOrder.objects.filter(status='completed').count(),
        'picked_up_orders': RepairOrder.objects.filter(status='picked_up').count(),
        'archived_orders': ArchivedOrder.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_devices': Device.objects.count(),
    }
    
    if request.user.profile.role == 'engineer':
        stats['my_assigned'] = RepairOrder.objects.filter(assigned_to=request.user).count()
        stats['my_pending'] = RepairOrder.objects.filter(assigned_to=request.user, status='pending').count()
        stats['my_repairing'] = RepairOrder.objects.filter(assigned_to=request.user, status='repairing').count()
    
    return Response(stats)
