from django.db import models
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from .models import RepairWorker, Repair, RepairLog
from .serializers import RepairWorkerSerializer, RepairSerializer, RepairLogSerializer


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner.user == request.user if obj.owner.user else False


class IsWorkerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.worker.user == request.user if hasattr(obj.worker, 'user') and obj.worker.user else False


class RepairWorkerViewSet(viewsets.ModelViewSet):
    queryset = RepairWorker.objects.all().order_by('-create_time')
    serializer_class = RepairWorkerSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        name = self.request.query_params.get('name')
        skill = self.request.query_params.get('skill')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if name:
            queryset = queryset.filter(name__contains=name)
        if skill:
            queryset = queryset.filter(skill__contains=skill)
        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        workers = self.queryset.filter(status='available')
        page = self.paginate_queryset(workers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(workers, many=True)
        return Response(serializer.data)


class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all().order_by('-create_time')
    serializer_class = RepairSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['destroy']:
            return [permissions.IsAdminUser()]
        if self.action in ['assign', 'start_repair', 'complete']:
            return [IsWorkerOrAdmin()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.request.query_params.get('owner_id')
        worker_id = self.request.query_params.get('worker_id')
        room_number = self.request.query_params.get('room_number')
        building_id = self.request.query_params.get('building_id')
        repair_type = self.request.query_params.get('repair_type')
        status_filter = self.request.query_params.get('status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        is_archived = self.request.query_params.get('is_archived')

        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        if worker_id:
            queryset = queryset.filter(worker_id=worker_id)
        if room_number:
            queryset = queryset.filter(house__room_number__contains=room_number)
        if building_id:
            queryset = queryset.filter(house__building_id=building_id)
        if repair_type:
            queryset = queryset.filter(repair_type=repair_type)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if start_date:
            queryset = queryset.filter(create_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(create_time__lte=f'{end_date} 23:59:59')
        if is_archived:
            queryset = queryset.filter(is_archived=(is_archived == 'true'))
        else:
            queryset = queryset.filter(is_archived=False)
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        repair = Repair.objects.get(id=response.data['id'])
        RepairLog.objects.create(
            repair=repair,
            action='创建工单',
            description=f'业主提交报修：{repair.title}',
            operator=repair.owner.name
        )
        return response

    @action(detail=False, methods=['get'])
    def by_owner(self, request):
        owner_id = request.query_params.get('owner_id')
        status_filter = request.query_params.get('status')
        if owner_id:
            repairs = self.queryset.filter(owner_id=owner_id)
            if status_filter:
                repairs = repairs.filter(status=status_filter)
            page = self.paginate_queryset(repairs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(repairs, many=True)
            return Response(serializer.data)
        return Response({'error': 'owner_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_worker(self, request):
        worker_id = request.query_params.get('worker_id')
        status_filter = request.query_params.get('status')
        if worker_id:
            repairs = self.queryset.filter(worker_id=worker_id)
            if status_filter:
                repairs = repairs.filter(status=status_filter)
            page = self.paginate_queryset(repairs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(repairs, many=True)
            return Response(serializer.data)
        return Response({'error': 'worker_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        repair = self.get_object()
        worker_id = request.data.get('worker_id')
        operator = request.data.get('operator', '系统管理员')

        if not worker_id:
            return Response({'error': 'worker_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            worker = RepairWorker.objects.get(id=worker_id)
        except RepairWorker.DoesNotExist:
            return Response({'error': 'Worker not found'}, status=status.HTTP_400_BAD_REQUEST)

        repair.worker = worker
        repair.status = 'assigned'
        repair.assign_time = datetime.now()
        repair.save()

        worker.status = 'busy'
        worker.save()

        RepairLog.objects.create(
            repair=repair,
            action='派单',
            description=f'指派维修人员：{worker.name}',
            operator=operator
        )

        serializer = self.get_serializer(repair)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def start_repair(self, request, pk=None):
        repair = self.get_object()
        operator = request.data.get('operator', repair.worker.name if repair.worker else '')

        repair.status = 'processing'
        repair.save()

        RepairLog.objects.create(
            repair=repair,
            action='开始维修',
            description='维修人员开始上门维修',
            operator=operator
        )

        serializer = self.get_serializer(repair)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        repair = self.get_object()
        repair_content = request.data.get('repair_content', '')
        cost = request.data.get('cost')
        operator = request.data.get('operator', repair.worker.name if repair.worker else '')
        auto_archive = request.data.get('auto_archive', True)

        repair.status = 'completed'
        repair.complete_time = datetime.now()
        repair.repair_content = repair_content
        if cost:
            repair.cost = cost
        
        if auto_archive:
            repair.is_archived = True
            repair.archived_time = datetime.now()
        
        repair.save()

        if repair.worker:
            repair.worker.status = 'available'
            repair.worker.save()

        RepairLog.objects.create(
            repair=repair,
            action='完成维修',
            description=f'维修完成：{repair_content}',
            operator=operator
        )

        if auto_archive:
            RepairLog.objects.create(
                repair=repair,
                action='自动归档',
                description='工单完成后系统自动归档',
                operator='系统'
            )

        serializer = self.get_serializer(repair)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': '只有管理员可以归档工单'}, status=status.HTTP_403_FORBIDDEN)
        
        repair = self.get_object()
        if repair.is_archived:
            return Response({'error': '工单已归档，请勿重复操作'}, status=status.HTTP_400_BAD_REQUEST)

        repair.is_archived = True
        repair.archived_time = datetime.now()
        repair.save()

        RepairLog.objects.create(
            repair=repair,
            action='手动归档',
            description='管理员手动归档工单',
            operator=request.user.username
        )

        serializer = self.get_serializer(repair)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': '只有管理员可以取消归档'}, status=status.HTTP_403_FORBIDDEN)
        
        repair = self.get_object()
        if not repair.is_archived:
            return Response({'error': '工单未归档'}, status=status.HTTP_400_BAD_REQUEST)

        repair.is_archived = False
        repair.archived_time = None
        repair.save()

        RepairLog.objects.create(
            repair=repair,
            action='取消归档',
            description='管理员取消归档工单',
            operator=request.user.username
        )

        serializer = self.get_serializer(repair)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        repair = self.get_object()
        rating = request.data.get('rating')
        feedback = request.data.get('feedback', '')

        if not rating or int(rating) < 1 or int(rating) > 5:
            return Response({'error': 'Valid rating (1-5) is required'}, status=status.HTTP_400_BAD_REQUEST)

        repair.rating = rating
        repair.feedback = feedback
        repair.save()

        RepairLog.objects.create(
            repair=repair,
            action='业主评价',
            description=f'评分：{rating}，评价：{feedback}',
            operator=repair.owner.name
        )

        serializer = self.get_serializer(repair)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        repair = self.get_object()
        reason = request.data.get('reason', '')
        operator = request.data.get('operator', repair.owner.name)

        repair.status = 'cancelled'
        repair.save()

        if repair.worker:
            repair.worker.status = 'available'
            repair.worker.save()

        RepairLog.objects.create(
            repair=repair,
            action='取消工单',
            description=f'取消原因：{reason}',
            operator=operator
        )

        serializer = self.get_serializer(repair)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        query = self.queryset
        if start_date:
            query = query.filter(create_time__gte=start_date)
        if end_date:
            query = query.filter(create_time__lte=f'{end_date} 23:59:59')
        
        by_status = {}
        for status_key in ['pending', 'assigned', 'processing', 'completed', 'cancelled']:
            by_status[status_key] = query.filter(status=status_key).count()
        
        by_type = {}
        for type_key in ['water', 'structure', 'equipment', 'other']:
            by_type[type_key] = query.filter(repair_type=type_key).count()
        
        return Response({
            'total_count': query.count(),
            'by_status': by_status,
            'by_type': by_type
        })


class RepairLogViewSet(viewsets.ModelViewSet):
    queryset = RepairLog.objects.all().order_by('-create_time')
    serializer_class = RepairLogSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        repair_id = self.request.query_params.get('repair_id')
        action = self.request.query_params.get('action')
        operator = self.request.query_params.get('operator')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if repair_id:
            queryset = queryset.filter(repair_id=repair_id)
        if action:
            queryset = queryset.filter(action__contains=action)
        if operator:
            queryset = queryset.filter(operator__contains=operator)
        if start_date:
            queryset = queryset.filter(create_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(create_time__lte=f'{end_date} 23:59:59')
        return queryset

    @action(detail=False, methods=['get'])
    def by_repair(self, request):
        repair_id = request.query_params.get('repair_id')
        if repair_id:
            logs = self.queryset.filter(repair_id=repair_id)
            page = self.paginate_queryset(logs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({'error': 'repair_id is required'}, status=status.HTTP_400_BAD_REQUEST)
