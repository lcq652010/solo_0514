import django_filters
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import RepairOrder, Customer, Device, Notification


class RepairOrderFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(method='filter_customer_name', label='客户姓名')
    customer_phone = django_filters.CharFilter(field_name='customer__phone', lookup_expr='icontains', label='客户电话')
    device_brand = django_filters.CharFilter(field_name='device__brand', lookup_expr='icontains', label='设备品牌')
    device_model = django_filters.CharFilter(field_name='device__model', lookup_expr='icontains', label='设备型号')
    device_type = django_filters.CharFilter(method='filter_device_type', label='设备类型')
    device_type_in = django_filters.CharFilter(method='filter_device_type_in', label='设备类型多选')
    status = django_filters.CharFilter(method='filter_status', label='工单状态')
    status_in = django_filters.CharFilter(method='filter_status_in', label='状态多选')
    created_at_start = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='创建时间开始')
    created_at_end = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='创建时间结束')
    completed_at_start = django_filters.DateFilter(field_name='completed_at', lookup_expr='gte', label='完成时间开始')
    completed_at_end = django_filters.DateFilter(field_name='completed_at', lookup_expr='lte', label='完成时间结束')
    picked_up_at_start = django_filters.DateFilter(field_name='picked_up_at', lookup_expr='gte', label='取机时间开始')
    picked_up_at_end = django_filters.DateFilter(field_name='picked_up_at', lookup_expr='lte', label='取机时间结束')
    assigned_to = django_filters.NumberFilter(field_name='assigned_to', lookup_expr='exact', label='分配工程师')
    assigned_to_isnull = django_filters.BooleanFilter(method='filter_assigned_to_isnull', label='是否未分配')
    created_by = django_filters.NumberFilter(field_name='created_by', lookup_expr='exact', label='创建人')
    min_cost = django_filters.NumberFilter(field_name='actual_cost', lookup_expr='gte', label='最小费用')
    max_cost = django_filters.NumberFilter(field_name='actual_cost', lookup_expr='lte', label='最大费用')
    has_cost = django_filters.BooleanFilter(method='filter_has_cost', label='是否有费用')
    search = django_filters.CharFilter(method='filter_search', label='综合搜索')
    order_number = django_filters.CharFilter(lookup_expr='icontains', label='工单号')
    fault_keyword = django_filters.CharFilter(field_name='fault_description', lookup_expr='icontains', label='故障关键词')
    is_overdue = django_filters.BooleanFilter(method='filter_is_overdue', label='是否超期')
    days_old = django_filters.NumberFilter(method='filter_days_old', label='创建天数')
    
    class Meta:
        model = RepairOrder
        fields = ['customer_name', 'customer_phone', 'device_brand', 'device_model', 'device_type', 
                  'device_type_in', 'status', 'status_in', 'created_at_start', 'created_at_end',
                  'completed_at_start', 'completed_at_end', 'picked_up_at_start', 'picked_up_at_end',
                  'assigned_to', 'assigned_to_isnull', 'created_by', 'min_cost', 'max_cost',
                  'has_cost', 'search', 'order_number', 'fault_keyword', 'is_overdue', 'days_old']
    
    def filter_customer_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(Q(customer__name__icontains=value))
    
    def filter_device_type(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(device__device_type=value)
    
    def filter_device_type_in(self, queryset, name, value):
        if not value:
            return queryset
        device_types = [t.strip() for t in value.split(',') if t.strip()]
        if device_types:
            return queryset.filter(device__device_type__in=device_types)
        return queryset
    
    def filter_status(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(status=value)
    
    def filter_status_in(self, queryset, name, value):
        if not value:
            return queryset
        status_list = [s.strip() for s in value.split(',') if s.strip()]
        if status_list:
            return queryset.filter(status__in=status_list)
        return queryset
    
    def filter_assigned_to_isnull(self, queryset, name, value):
        if value is True:
            return queryset.filter(assigned_to__isnull=True)
        elif value is False:
            return queryset.filter(assigned_to__isnull=False)
        return queryset
    
    def filter_has_cost(self, queryset, name, value):
        if value is True:
            return queryset.filter(actual_cost__isnull=False)
        elif value is False:
            return queryset.filter(Q(actual_cost__isnull=True) | Q(actual_cost=0))
        return queryset
    
    def filter_is_overdue(self, queryset, name, value):
        if value is True:
            seven_days_ago = timezone.now() - timedelta(days=7)
            return queryset.filter(
                created_at__lt=seven_days_ago,
                status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
            )
        elif value is False:
            seven_days_ago = timezone.now() - timedelta(days=7)
            return queryset.exclude(
                created_at__lt=seven_days_ago,
                status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
            )
        return queryset
    
    def filter_days_old(self, queryset, name, value):
        if not value:
            return queryset
        cutoff_date = timezone.now() - timedelta(days=value)
        return queryset.filter(created_at__lte=cutoff_date)
    
    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(order_number__icontains=value) |
            Q(customer__name__icontains=value) |
            Q(customer__phone__icontains=value) |
            Q(device__brand__icontains=value) |
            Q(device__model__icontains=value) |
            Q(device__serial_number__icontains=value) |
            Q(fault_description__icontains=value)
        )


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='姓名')
    phone = django_filters.CharFilter(lookup_expr='icontains', label='电话')
    email = django_filters.CharFilter(lookup_expr='icontains', label='邮箱')
    address = django_filters.CharFilter(lookup_expr='icontains', label='地址')
    search = django_filters.CharFilter(method='filter_search', label='综合搜索')
    created_at_start = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='创建时间开始')
    created_at_end = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='创建时间结束')
    has_device = django_filters.BooleanFilter(method='filter_has_device', label='是否有设备')
    has_active_order = django_filters.BooleanFilter(method='filter_has_active_order', label='是否有活跃工单')
    min_devices = django_filters.NumberFilter(method='filter_min_devices', label='最少设备数')
    
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'search', 'created_at_start', 
                  'created_at_end', 'has_device', 'has_active_order', 'min_devices']
    
    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(phone__icontains=value) |
            Q(email__icontains=value) |
            Q(address__icontains=value)
        )
    
    def filter_has_device(self, queryset, name, value):
        if value is True:
            return queryset.filter(devices__isnull=False).distinct()
        elif value is False:
            return queryset.filter(devices__isnull=True).distinct()
        return queryset
    
    def filter_has_active_order(self, queryset, name, value):
        if value is True:
            return queryset.filter(
                repair_orders__status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
            ).distinct()
        elif value is False:
            return queryset.exclude(
                repair_orders__status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
            ).distinct()
        return queryset
    
    def filter_min_devices(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.annotate(
            device_count=Count('devices')
        ).filter(device_count__gte=value).distinct()


class DeviceFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains', label='客户姓名')
    customer_phone = django_filters.CharFilter(field_name='customer__phone', lookup_expr='icontains', label='客户电话')
    brand = django_filters.CharFilter(lookup_expr='icontains', label='品牌')
    model = django_filters.CharFilter(lookup_expr='icontains', label='型号')
    serial_number = django_filters.CharFilter(lookup_expr='icontains', label='序列号')
    device_type = django_filters.CharFilter(method='filter_device_type', label='设备类型')
    device_type_in = django_filters.CharFilter(method='filter_device_type_in', label='设备类型多选')
    search = django_filters.CharFilter(method='filter_search', label='综合搜索')
    created_at_start = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='创建时间开始')
    created_at_end = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='创建时间结束')
    has_active_order = django_filters.BooleanFilter(method='filter_has_active_order', label='是否有活跃工单')
    description = django_filters.CharFilter(lookup_expr='icontains', label='设备描述关键词')
    
    class Meta:
        model = Device
        fields = ['customer_name', 'customer_phone', 'brand', 'model', 'serial_number', 
                  'device_type', 'device_type_in', 'search', 'created_at_start', 'created_at_end',
                  'has_active_order', 'description']
    
    def filter_device_type(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(device_type=value)
    
    def filter_device_type_in(self, queryset, name, value):
        if not value:
            return queryset
        device_types = [t.strip() for t in value.split(',') if t.strip()]
        if device_types:
            return queryset.filter(device_type__in=device_types)
        return queryset
    
    def filter_has_active_order(self, queryset, name, value):
        if value is True:
            return queryset.filter(
                repair_orders__status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
            ).distinct()
        elif value is False:
            return queryset.exclude(
                repair_orders__status__in=['pending', 'diagnosing', 'repairing', 'waiting_parts']
            ).distinct()
        return queryset
    
    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(brand__icontains=value) |
            Q(model__icontains=value) |
            Q(serial_number__icontains=value) |
            Q(customer__name__icontains=value) |
            Q(description__icontains=value)
        )


class NotificationFilter(django_filters.FilterSet):
    is_read = django_filters.BooleanFilter(label='是否已读')
    notification_type = django_filters.CharFilter(lookup_expr='exact', label='通知类型')
    notification_type_in = django_filters.CharFilter(method='filter_type_in', label='通知类型多选')
    created_at_start = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='创建时间开始')
    created_at_end = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='创建时间结束')
    search = django_filters.CharFilter(method='filter_search', label='搜索')
    
    class Meta:
        model = Notification
        fields = ['is_read', 'notification_type', 'notification_type_in', 
                  'created_at_start', 'created_at_end', 'search']
    
    def filter_type_in(self, queryset, name, value):
        if not value:
            return queryset
        types = [t.strip() for t in value.split(',') if t.strip()]
        if types:
            return queryset.filter(notification_type__in=types)
        return queryset
    
    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title__icontains=value) |
            Q(content__icontains=value)
        )
