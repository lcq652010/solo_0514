from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta

from .models import Institution, Device, Rental, Calibration, DamageRecord, MaintenanceRecord, ReturnAcceptance, Settlement
from .serializers import (
    InstitutionSerializer,
    DeviceSerializer,
    RentalSerializer,
    CalibrationSerializer,
    DamageRecordSerializer,
    MaintenanceRecordSerializer,
    ReturnAcceptanceSerializer,
    SettlementSerializer,
)


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    filterset_fields = ['is_active']
    search_fields = ['name', 'contact_person', 'contact_phone']


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filterset_fields = ['device_type', 'use_department', 'status']
    search_fields = ['name', 'model', 'serial_number', 'manufacturer']

    def get_queryset(self):
        queryset = super().get_queryset()
        today = timezone.now().date()

        calibration_status = self.request.query_params.get('calibration_status')
        if calibration_status:
            if calibration_status == 'expired':
                queryset = queryset.filter(
                    Q(next_calibration_date__lte=today) | Q(next_calibration_date__isnull=True)
                )
            elif calibration_status == 'urgent':
                queryset = queryset.filter(
                    next_calibration_date__gt=today,
                    next_calibration_date__lte=today + timedelta(days=7)
                )
            elif calibration_status == 'warning':
                queryset = queryset.filter(
                    next_calibration_date__gt=today + timedelta(days=7),
                    next_calibration_date__lte=today + timedelta(days=30)
                )
            elif calibration_status == 'normal':
                queryset = queryset.filter(
                    next_calibration_date__gt=today + timedelta(days=30)
                )

        return queryset

    @action(detail=False, methods=['get'])
    def filters(self, request):
        device_types = [{'value': key, 'label': label} for key, label in Device.DEVICE_TYPE_CHOICES]
        departments = [{'value': key, 'label': label} for key, label in Device.USE_DEPARTMENT_CHOICES]
        statuses = [{'value': key, 'label': label} for key, label in Device.DEVICE_STATUS_CHOICES]
        calibration_statuses = [
            {'value': 'normal', 'label': '正常'},
            {'value': 'warning', 'label': '提醒(30天内)'},
            {'value': 'urgent', 'label': '紧急(7天内)'},
            {'value': 'expired', 'label': '已过期'},
        ]
        return Response({
            'device_types': device_types,
            'departments': departments,
            'statuses': statuses,
            'calibration_statuses': calibration_statuses,
        })

    @action(detail=False, methods=['get'])
    def utilization_stats(self, request):
        days = int(request.query_params.get('days', 30))
        devices = Device.objects.all()
        
        utilization_rates = []
        for device in devices:
            utilization_rates.append({
                'device_id': device.id,
                'device_name': device.name,
                'device_type': device.device_type,
                'utilization_rate': device.get_utilization_rate(days=days),
                'total_rental_days': device.get_total_rental_days(),
                'total_revenue': device.get_total_rental_revenue(),
            })
        
        utilization_rates.sort(key=lambda x: x['utilization_rate'], reverse=True)
        
        avg_utilization = sum(item['utilization_rate'] for item in utilization_rates) / len(utilization_rates) if utilization_rates else 0
        
        return Response({
            'days': days,
            'avg_utilization': round(avg_utilization, 2),
            'device_utilization': utilization_rates,
        })

    @action(detail=False, methods=['get'])
    def calibration_alerts(self, request):
        today = timezone.now().date()
        expired = Device.objects.filter(
            Q(next_calibration_date__lte=today) | Q(next_calibration_date__isnull=True)
        ).count()
        urgent = Device.objects.filter(
            next_calibration_date__gt=today,
            next_calibration_date__lte=today + timedelta(days=7)
        ).count()
        warning = Device.objects.filter(
            next_calibration_date__gt=today + timedelta(days=7),
            next_calibration_date__lte=today + timedelta(days=30)
        ).count()
        return Response({
            'expired': expired,
            'urgent': urgent,
            'warning': warning,
            'total': expired + urgent + warning,
        })

    @action(detail=True, methods=['post'])
    def start_rental(self, request, pk=None):
        device = self.get_object()
        if device.start_rental():
            return Response({'status': 'success', 'message': '设备已进入租赁状态'})
        return Response(
            {'status': 'error', 'message': '设备状态不允许租赁或校准已过期'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def end_rental(self, request, pk=None):
        device = self.get_object()
        if device.end_rental():
            return Response({'status': 'success', 'message': '设备已从租赁状态收回'})
        return Response(
            {'status': 'error', 'message': '设备当前不在租赁状态'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def start_calibration(self, request, pk=None):
        device = self.get_object()
        if device.start_calibration():
            return Response({'status': 'success', 'message': '设备已进入校准状态'})
        return Response(
            {'status': 'error', 'message': '设备状态不允许进入校准'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def complete_calibration(self, request, pk=None):
        device = self.get_object()
        calibration_date = request.data.get('calibration_date')
        if device.complete_calibration(calibration_date):
            return Response({'status': 'success', 'message': '设备校准完成，已恢复可用状态'})
        return Response(
            {'status': 'error', 'message': '设备当前不在校准状态'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def start_maintenance(self, request, pk=None):
        device = self.get_object()
        if device.start_maintenance():
            return Response({'status': 'success', 'message': '设备已进入维修状态'})
        return Response(
            {'status': 'error', 'message': '设备状态不允许进入维修'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def complete_maintenance(self, request, pk=None):
        device = self.get_object()
        if device.complete_maintenance():
            return Response({'status': 'success', 'message': '设备维修完成，已恢复可用状态'})
        return Response(
            {'status': 'error', 'message': '设备当前不在维修状态'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def retire(self, request, pk=None):
        device = self.get_object()
        if device.retire():
            return Response({'status': 'success', 'message': '设备已报废'})
        return Response(
            {'status': 'error', 'message': '设备正在租赁中，无法报废'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    filterset_fields = ['status', 'institution', 'device']
    search_fields = ['rental_no', 'contact_person', 'contact_phone']

    def get_queryset(self):
        queryset = super().get_queryset()
        today = timezone.now().date()

        countdown_status = self.request.query_params.get('countdown_status')
        if countdown_status:
            if countdown_status == 'overdue':
                queryset = queryset.filter(
                    status='active',
                    end_date__lte=today
                )
            elif countdown_status == 'urgent':
                queryset = queryset.filter(
                    status='active',
                    end_date__gt=today,
                    end_date__lte=today + timedelta(days=1)
                )
            elif countdown_status == 'warning':
                queryset = queryset.filter(
                    status='active',
                    end_date__gt=today + timedelta(days=1),
                    end_date__lte=today + timedelta(days=3)
                )
            elif countdown_status == 'normal':
                queryset = queryset.filter(
                    status='active',
                    end_date__gt=today + timedelta(days=3)
                )

        start_date_from = self.request.query_params.get('start_date_from')
        if start_date_from:
            queryset = queryset.filter(start_date__gte=start_date_from)
        start_date_to = self.request.query_params.get('start_date_to')
        if start_date_to:
            queryset = queryset.filter(start_date__lte=start_date_to)
        end_date_from = self.request.query_params.get('end_date_from')
        if end_date_from:
            queryset = queryset.filter(end_date__gte=end_date_from)
        end_date_to = self.request.query_params.get('end_date_to')
        if end_date_to:
            queryset = queryset.filter(end_date__lte=end_date_to)

        return queryset

    def perform_create(self, serializer):
        device = serializer.validated_data['device']
        if not device.can_be_rented():
            raise serializers.ValidationError({'error': '该设备当前不可租赁或校准已过期'})
        serializer.save()

    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        rental = self.get_object()
        renewal_days = request.data.get('renewal_days')
        new_daily_fee = request.data.get('new_daily_fee')

        if not renewal_days:
            return Response(
                {'status': 'error', 'message': '请输入续租天数'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            renewal_days = int(renewal_days)
            if renewal_days <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return Response(
                {'status': 'error', 'message': '续租天数必须是正整数'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_rental, message = rental.renew(renewal_days, new_daily_fee)
        if new_rental:
            return Response({
                'status': 'success',
                'message': message,
                'new_rental_no': new_rental.rental_no,
                'new_start_date': new_rental.start_date,
                'new_end_date': new_rental.end_date,
            })
        return Response({'status': 'error', 'message': message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        rental = self.get_object()
        approval_notes = request.data.get('approval_notes', '')
        if rental.approve(approval_notes):
            return Response({'status': 'success', 'message': '审批通过'})
        return Response(
            {'status': 'error', 'message': '该租赁申请状态不允许审批'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def start_rental(self, request, pk=None):
        rental = self.get_object()
        actual_start_date = request.data.get('actual_start_date')
        if rental.start(actual_start_date):
            return Response({'status': 'success', 'message': '租赁已开始'})
        return Response(
            {'status': 'error', 'message': '该租赁状态不允许开始或设备状态异常'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def return_device(self, request, pk=None):
        rental = self.get_object()
        return_date = request.data.get('return_date')
        inspector = request.data.get('inspector', '')
        if rental.return_device(return_date, inspector):
            return Response({
                'status': 'success',
                'message': '设备已归还',
                'actual_days': rental.actual_days,
                'overtime_days': rental.overtime_days,
                'overtime_fee': float(rental.overtime_fee),
                'actual_total': float(rental.actual_total),
            })
        return Response(
            {'status': 'error', 'message': '该租赁状态不允许归还'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        rental = self.get_object()
        if rental.cancel():
            return Response({'status': 'success', 'message': '租赁已取消'})
        return Response(
            {'status': 'error', 'message': '该租赁状态不允许取消'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def rental_alerts(self, request):
        today = timezone.now().date()
        overdue = Rental.objects.filter(
            status='active',
            end_date__lte=today
        ).count()
        urgent = Rental.objects.filter(
            status='active',
            end_date__gt=today,
            end_date__lte=today + timedelta(days=1)
        ).count()
        warning = Rental.objects.filter(
            status='active',
            end_date__gt=today + timedelta(days=1),
            end_date__lte=today + timedelta(days=3)
        ).count()
        return Response({
            'overdue': overdue,
            'urgent': urgent,
            'warning': warning,
            'total': overdue + urgent + warning,
        })


class DamageRecordViewSet(viewsets.ModelViewSet):
    queryset = DamageRecord.objects.all()
    serializer_class = DamageRecordSerializer
    filterset_fields = ['damage_type', 'damage_level', 'needs_maintenance', 'device', 'rental']
    search_fields = ['damage_description', 'inspector']


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer
    filterset_fields = ['status', 'maintenance_type', 'device']
    search_fields = ['maintenance_content', 'reporter', 'maintenance_person']

    @action(detail=True, methods=['post'])
    def start_maintenance(self, request, pk=None):
        maintenance = self.get_object()
        maintenance_person = request.data.get('maintenance_person', '')
        start_date = request.data.get('start_date')
        if maintenance.start_maintenance(maintenance_person, start_date):
            return Response({'status': 'success', 'message': '维修已开始'})
        return Response(
            {'status': 'error', 'message': '该维修状态不允许开始'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def complete_maintenance(self, request, pk=None):
        maintenance = self.get_object()
        maintenance_result = request.data.get('maintenance_result', '')
        parts_cost = request.data.get('parts_cost')
        labor_cost = request.data.get('labor_cost')
        complete_date = request.data.get('complete_date')

        if parts_cost:
            parts_cost = float(parts_cost)
        if labor_cost:
            labor_cost = float(labor_cost)

        if maintenance.complete_maintenance(maintenance_result, parts_cost, labor_cost, complete_date):
            return Response({'status': 'success', 'message': '维修已完成'})
        return Response(
            {'status': 'error', 'message': '该维修状态不允许完成'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CalibrationViewSet(viewsets.ModelViewSet):
    queryset = Calibration.objects.all()
    serializer_class = CalibrationSerializer
    filterset_fields = ['status', 'device']
    search_fields = ['calibrator', 'calibration_agency', 'certificate_no']

    @action(detail=True, methods=['post'])
    def start_calibration(self, request, pk=None):
        calibration = self.get_object()
        if calibration.start_calibration():
            return Response({'status': 'success', 'message': '校准已开始，设备进入校准状态'})
        return Response(
            {'status': 'error', 'message': '校准状态不允许开始或设备状态异常'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def complete_calibration(self, request, pk=None):
        calibration = self.get_object()
        calibration_result = request.data.get('calibration_result', '')
        next_calibration_date = request.data.get('next_calibration_date')
        if calibration.complete_calibration(calibration_result, next_calibration_date):
            return Response({'status': 'success', 'message': '校准已完成，设备已恢复可用状态'})
        return Response(
            {'status': 'error', 'message': '校准状态不允许完成'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def fail_calibration(self, request, pk=None):
        calibration = self.get_object()
        calibration_result = request.data.get('calibration_result', '')
        if calibration.fail_calibration(calibration_result):
            return Response({'status': 'success', 'message': '校准未通过，设备进入维修状态'})
        return Response(
            {'status': 'error', 'message': '校准状态不允许标记未通过'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ReturnAcceptanceViewSet(viewsets.ModelViewSet):
    queryset = ReturnAcceptance.objects.all()
    serializer_class = ReturnAcceptanceSerializer
    filterset_fields = ['status']

    def perform_create(self, serializer):
        acceptance = serializer.save()
        rental = acceptance.rental

        rental.actual_end_date = acceptance.return_date
        rental.actual_days = (acceptance.return_date - rental.actual_start_date).days + 1

        planned_end = rental.end_date
        overtime_days = max(0, (acceptance.return_date - planned_end).days)
        overtime_fee = round(overtime_days * rental.daily_fee * 1.5, 2)
        normal_days = rental.actual_days - overtime_days
        normal_fee = normal_days * rental.daily_fee
        actual_total = normal_fee + overtime_fee

        rental.overtime_days = overtime_days
        rental.overtime_fee = overtime_fee
        rental.actual_total = actual_total
        rental.status = 'returned'
        rental.device.end_rental()
        rental.save()

        Settlement.objects.create(
            rental=rental,
            acceptance=acceptance,
            rental_days=rental.actual_days,
            rental_fee=float(normal_fee),
            overtime_days=overtime_days,
            overtime_fee=overtime_fee,
            damage_fee=acceptance.damage_fee,
            other_fee=0,
            total_amount=float(normal_fee) + float(overtime_fee) + float(acceptance.damage_fee)
        )

    @action(detail=True, methods=['post'])
    def create_damage_record(self, request, pk=None):
        acceptance = self.get_object()
        damage_type = request.data.get('damage_type')
        damage_level = request.data.get('damage_level')
        damage_description = request.data.get('damage_description', '')
        estimated_repair_cost = request.data.get('estimated_repair_cost', 0)

        if not all([damage_type, damage_level]):
            return Response(
                {'status': 'error', 'message': '请填写完整的损坏信息'},
                status=status.HTTP_400_BAD_REQUEST
            )

        damage_record = acceptance.create_damage_record(
            damage_type=damage_type,
            damage_level=damage_level,
            damage_description=damage_description,
            estimated_repair_cost=float(estimated_repair_cost)
        )
        return Response({
            'status': 'success',
            'message': '损耗记录已创建',
            'damage_record_id': damage_record.id,
        })

    @action(detail=True, methods=['post'])
    def create_maintenance_record(self, request, pk=None):
        acceptance = self.get_object()
        maintenance_type = request.data.get('maintenance_type', 'damage')
        reporter = request.data.get('reporter', '')
        maintenance_content = request.data.get('maintenance_content', '')

        if not acceptance.damage_record:
            return Response(
                {'status': 'error', 'message': '请先创建损耗记录'},
                status=status.HTTP_400_BAD_REQUEST
            )

        maintenance_record = acceptance.create_maintenance_record(
            maintenance_type=maintenance_type,
            reporter=reporter,
            maintenance_content=maintenance_content
        )
        return Response({
            'status': 'success',
            'message': '维修记录已创建',
            'maintenance_record_id': maintenance_record.id,
        })


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    filterset_fields = ['status', 'payment_method']
    search_fields = ['invoice_no']

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        settlement = self.get_object()
        payment_method = request.data.get('payment_method')
        payment_date = request.data.get('payment_date')
        invoice_no = request.data.get('invoice_no', '')

        if not payment_method:
            return Response(
                {'status': 'error', 'message': '请选择付款方式'},
                status=status.HTTP_400_BAD_REQUEST
            )

        settlement.payment_method = payment_method
        if payment_date:
            from datetime import datetime
            settlement.payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
        else:
            settlement.payment_date = timezone.now().date()
        settlement.invoice_no = invoice_no
        settlement.status = 'paid'
        settlement.save()

        settlement.rental.complete()
        return Response({'status': 'success', 'message': '已标记为已付款'})


class DashboardViewSet(viewsets.ViewSet):
    def list(self, request):
        today = timezone.now().date()

        device_stats = Device.objects.aggregate(
            total=Count('id'),
            available=Count('id', filter=Q(status='available')),
            rented=Count('id', filter=Q(status='rented')),
            calibrating=Count('id', filter=Q(status='calibrating')),
            maintenance=Count('id', filter=Q(status='maintenance')),
            retired=Count('id', filter=Q(status='retired')),
        )

        devices_need_calibration = Device.objects.filter(
            Q(next_calibration_date__lte=today) | Q(next_calibration_date__isnull=True)
        ).count()

        upcoming_calibrations = Device.objects.filter(
            next_calibration_date__lte=today + timedelta(days=30),
            next_calibration_date__gt=today
        ).count()

        rental_stats = Rental.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            approved=Count('id', filter=Q(status='approved')),
            active=Count('id', filter=Q(status='active')),
            returned=Count('id', filter=Q(status='returned')),
            completed=Count('id', filter=Q(status='completed')),
            renewed=Count('id', filter=Q(status='renewed')),
            cancelled=Count('id', filter=Q(status='cancelled')),
        )

        overdue_rentals = Rental.objects.filter(
            status='active',
            end_date__lte=today
        ).count()

        upcoming_returns = Rental.objects.filter(
            status='active',
            end_date__lte=today + timedelta(days=3),
            end_date__gt=today
        ).count()

        settlement_stats = Settlement.objects.filter(status='paid').aggregate(
            total_revenue=Sum('total_amount'),
            total_rental_fee=Sum('rental_fee'),
            total_overtime_fee=Sum('overtime_fee'),
            total_damage_fee=Sum('damage_fee'),
        )

        maintenance_stats = MaintenanceRecord.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            in_progress=Count('id', filter=Q(status='in_progress')),
            completed=Count('id', filter=Q(status='completed')),
            total_cost=Sum('total_cost'),
        )

        avg_utilization_30d = Device.objects.all().aggregate(
            avg_utilization=Avg('id')
        )['avg_utilization'] or 0
        
        devices = Device.objects.all()
        total_utilization = 0
        count = 0
        for device in devices:
            total_utilization += device.get_utilization_rate(days=30)
            count += 1
        avg_utilization_30d = round(total_utilization / count, 2) if count > 0 else 0

        institution_count = Institution.objects.filter(is_active=True).count()

        data = {
            'device_stats': device_stats,
            'devices_need_calibration': devices_need_calibration,
            'upcoming_calibrations': upcoming_calibrations,
            'avg_utilization_30d': avg_utilization_30d,
            'rental_stats': rental_stats,
            'overdue_rentals': overdue_rentals,
            'upcoming_returns': upcoming_returns,
            'total_revenue': float(settlement_stats['total_revenue'] or 0),
            'total_rental_fee': float(settlement_stats['total_rental_fee'] or 0),
            'total_overtime_fee': float(settlement_stats['total_overtime_fee'] or 0),
            'total_damage_fee': float(settlement_stats['total_damage_fee'] or 0),
            'maintenance_stats': {
                'total': maintenance_stats['total'],
                'pending': maintenance_stats['pending'],
                'in_progress': maintenance_stats['in_progress'],
                'completed': maintenance_stats['completed'],
                'total_cost': float(maintenance_stats['total_cost'] or 0),
            },
            'institution_count': institution_count,
        }

        return Response(data)
