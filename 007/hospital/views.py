from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from .permissions import *


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """获取当前用户信息"""
    try:
        staff = request.user.staff
        return Response({
            'user_id': request.user.id,
            'username': request.user.username,
            'name': staff.name,
            'role': staff.role,
            'role_display': staff.get_role_display(),
            'phone': staff.phone,
            'department': staff.department.name if staff.department else None
        })
    except:
        return Response({
            'user_id': request.user.id,
            'username': request.user.username,
            'name': request.user.username,
            'role': 'admin' if request.user.is_superuser else 'unknown',
            'role_display': '超级管理员' if request.user.is_superuser else '未知'
        })


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = Staff.objects.all()
        name = self.request.query_params.get('name')
        role = self.request.query_params.get('role')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Doctor.objects.all()
        name = self.request.query_params.get('name')
        department_id = self.request.query_params.get('department_id')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsReceptionistOrDoctor]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Owner.objects.all()
        name = self.request.query_params.get('name')
        phone = self.request.query_params.get('phone')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.data.get('name'):
            return Response({'error': '姓名不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('phone'):
            return Response({'error': '电话不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsReceptionistOrDoctor]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Pet.objects.all()
        name = self.request.query_params.get('name')
        owner_name = self.request.query_params.get('owner_name')
        species = self.request.query_params.get('species')
        gender = self.request.query_params.get('gender')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if owner_name:
            queryset = queryset.filter(owner__name__icontains=owner_name)
        if species:
            queryset = queryset.filter(species__icontains=species)
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset

    def create(self, request, *args, **kwargs):
        required_fields = ['name', 'species', 'gender', 'age', 'weight', 'owner']
        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} 不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            age = int(request.data.get('age'))
            if age < 0 or age > 50:
                return Response({'error': '年龄必须在0-50之间'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': '年龄必须是有效的数字'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            weight = float(request.data.get('weight'))
            if weight < 0 or weight > 200:
                return Response({'error': '体重必须在0-200kg之间'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': '体重必须是有效的数字'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsDoctorOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Medicine.objects.all()
        name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')
        low_stock = self.request.query_params.get('low_stock')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)
        if low_stock:
            queryset = queryset.filter(stock__lte=10)
        return queryset

    def create(self, request, *args, **kwargs):
        required_fields = ['name', 'category', 'specification', 'unit', 'price', 'stock', 'expiry_date']
        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} 不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            price = float(request.data.get('price'))
            if price < 0:
                return Response({'error': '价格不能为负数'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': '价格必须是有效的数字'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            stock = int(request.data.get('stock'))
            if stock < 0:
                return Response({'error': '库存不能为负数'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': '库存必须是有效的整数'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'cancel']:
            permission_classes = [IsReceptionistOrDoctor]
        else:
            permission_classes = [IsDoctorOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Visit.objects.all()
        pet_name = self.request.query_params.get('pet_name')
        owner_name = self.request.query_params.get('owner_name')
        status = self.request.query_params.get('status')
        doctor_id = self.request.query_params.get('doctor_id')
        department_id = self.request.query_params.get('department_id')
        visit_no = self.request.query_params.get('visit_no')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if pet_name:
            queryset = queryset.filter(pet__name__icontains=pet_name)
        if owner_name:
            queryset = queryset.filter(pet__owner__name__icontains=owner_name)
        if status:
            queryset = queryset.filter(status=status)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        if visit_no:
            queryset = queryset.filter(visit_no__icontains=visit_no)
        if date_from:
            queryset = queryset.filter(appointment_time__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(appointment_time__date__lte=date_to)
        
        try:
            if not self.request.user.is_superuser and self.request.user.staff.role == 'doctor':
                doctor = Doctor.objects.filter(staff__user=self.request.user).first()
                if doctor:
                    queryset = queryset.filter(doctor=doctor)
        except:
            pass
        
        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        required_fields = ['pet', 'doctor', 'department', 'symptom', 'appointment_time']
        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} 不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pet_id = int(request.data.get('pet'))
            if not Pet.objects.filter(id=pet_id).exists():
                return Response({'error': '指定的宠物不存在'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': '宠物ID格式错误'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            doctor_id = int(request.data.get('doctor'))
            if not Doctor.objects.filter(id=doctor_id).exists():
                return Response({'error': '指定的医生不存在'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': '医生ID格式错误'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def start_treatment(self, request, pk=None):
        visit = self.get_object()
        if visit.status == 'pending':
            visit.status = 'in_progress'
            visit.save()
            return Response({
                'status': 'success', 
                'message': '开始诊疗',
                'visit_no': visit.visit_no
            })
        return Response(
            {'status': 'error', 'message': f'当前状态为"{visit.get_status_display()}"，无法开始诊疗'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        visit = self.get_object()
        if visit.status == 'in_progress':
            visit.status = 'completed'
            visit.completed_at = timezone.now()
            visit.save()
            
            medicine_fee = 0
            try:
                medical_record = MedicalRecord.objects.get(visit=visit)
                prescriptions = Prescription.objects.filter(medical_record=medical_record)
                for p in prescriptions:
                    medicine_fee += float(p.subtotal)
            except MedicalRecord.DoesNotExist:
                pass
            
            Charge.objects.create(
                visit=visit,
                registration_fee=visit.registration_fee,
                medicine_fee=medicine_fee,
                treatment_fee=visit.treatment_fee,
                other_fee=0,
                total_amount=visit.registration_fee + medicine_fee + visit.treatment_fee
            )
            
            return Response({
                'status': 'success', 
                'message': '诊疗完成，已自动生成结算单',
                'visit_no': visit.visit_no
            })
        return Response(
            {'status': 'error', 'message': f'当前状态为"{visit.get_status_display()}"，无法完成诊疗'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        visit = self.get_object()
        if visit.status in ['pending', 'in_progress']:
            visit.status = 'cancelled'
            visit.save()
            return Response({
                'status': 'success', 
                'message': '已取消就诊',
                'visit_no': visit.visit_no
            })
        return Response(
            {'status': 'error', 'message': f'当前状态为"{visit.get_status_display()}"，无法取消'},
            status=status.HTTP_400_BAD_REQUEST
        )


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsDoctorOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = MedicalRecord.objects.all()
        visit_no = self.request.query_params.get('visit_no')
        pet_name = self.request.query_params.get('pet_name')
        diagnosis = self.request.query_params.get('diagnosis')
        if visit_no:
            queryset = queryset.filter(visit__visit_no__icontains=visit_no)
        if pet_name:
            queryset = queryset.filter(visit__pet__name__icontains=pet_name)
        if diagnosis:
            queryset = queryset.filter(diagnosis__icontains=diagnosis)
        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        required_fields = ['visit', 'chief_complaint', 'physical_exam', 'diagnosis', 'treatment_plan']
        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} 不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            visit_id = int(request.data.get('visit'))
            if not Visit.objects.filter(id=visit_id).exists():
                return Response({'error': '指定的就诊记录不存在'}, status=status.HTTP_400_BAD_REQUEST)
            if MedicalRecord.objects.filter(visit_id=visit_id).exists():
                return Response({'error': '该就诊记录已存在病历'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': '就诊ID格式错误'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsDoctorOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Prescription.objects.all()
        medical_record_id = self.request.query_params.get('medical_record_id')
        medicine_name = self.request.query_params.get('medicine_name')
        if medical_record_id:
            queryset = queryset.filter(medical_record_id=medical_record_id)
        if medicine_name:
            queryset = queryset.filter(medicine__name__icontains=medicine_name)
        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        required_fields = ['medical_record', 'medicine', 'quantity', 'dosage']
        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} 不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            medicine_id = int(request.data.get('medicine'))
            quantity = int(request.data.get('quantity'))
            medicine = Medicine.objects.get(id=medicine_id)
            if quantity <= 0:
                return Response({'error': '数量必须大于0'}, status=status.HTTP_400_BAD_REQUEST)
            if medicine.stock < quantity:
                return Response(
                    {'error': f'药品库存不足，当前库存: {medicine.stock}, 需要: {quantity}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            stock_before = medicine.stock
            medicine.stock -= quantity
            medicine.save()
            
            staff = None
            try:
                staff = request.user.staff
            except:
                pass
            
            try:
                medical_record = MedicalRecord.objects.get(id=request.data.get('medical_record'))
                related_visit = medical_record.visit
            except:
                related_visit = None
            
            InventoryLog.objects.create(
                medicine=medicine,
                operation='out',
                quantity=quantity,
                stock_before=stock_before,
                stock_after=medicine.stock,
                related_visit=related_visit,
                operator=staff,
                remark='处方开药'
            )
            
        except Medicine.DoesNotExist:
            return Response({'error': '指定的药品不存在'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'error': '药品ID或数量格式错误'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        prescription = self.get_object()
        medicine = prescription.medicine
        stock_before = medicine.stock
        quantity = prescription.quantity
        
        medicine.stock += quantity
        medicine.save()
        
        staff = None
        try:
            staff = request.user.staff
        except:
            pass
        
        InventoryLog.objects.create(
            medicine=medicine,
            operation='refund',
            quantity=quantity,
            stock_before=stock_before,
            stock_after=medicine.stock,
            related_visit=prescription.medical_record.visit,
            operator=staff,
            remark='删除处方退库'
        )
        
        return super().destroy(request, *args, **kwargs)


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'pay':
            permission_classes = [IsReceptionistOrDoctor]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Charge.objects.all()
        charge_no = self.request.query_params.get('charge_no')
        visit_no = self.request.query_params.get('visit_no')
        status = self.request.query_params.get('status')
        payment_method = self.request.query_params.get('payment_method')
        if charge_no:
            queryset = queryset.filter(charge_no__icontains=charge_no)
        if visit_no:
            queryset = queryset.filter(visit__visit_no__icontains=visit_no)
        if status:
            queryset = queryset.filter(status=status)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        charge = self.get_object()
        if charge.status == 'unpaid':
            payment_method = request.data.get('payment_method', 'wechat')
            if payment_method not in ['cash', 'wechat', 'alipay', 'card']:
                return Response({'error': '无效的支付方式'}, status=status.HTTP_400_BAD_REQUEST)
            charge.status = 'paid'
            charge.payment_method = payment_method
            charge.paid_at = timezone.now()
            charge.save()
            return Response({
                'status': 'success',
                'message': '支付成功',
                'charge_no': charge.charge_no,
                'total_amount': float(charge.total_amount),
                'payment_method': charge.get_payment_method_display(),
                'paid_at': charge.paid_at
            })
        return Response(
            {'status': 'error', 'message': f'当前状态为"{charge.get_status_display()}"，无法支付'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        charge = self.get_object()
        if charge.status == 'paid':
            charge.status = 'refunded'
            charge.save()
            return Response({
                'status': 'success',
                'message': '退款成功',
                'charge_no': charge.charge_no
            })
        return Response(
            {'status': 'error', 'message': f'当前状态为"{charge.get_status_display()}"，无法退款'},
            status=status.HTTP_400_BAD_REQUEST
        )


class InventoryLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer
    pagination_class = StandardPagination
    permission_classes = [IsDoctorOrAdmin]

    def get_queryset(self):
        queryset = InventoryLog.objects.all()
        medicine_name = self.request.query_params.get('medicine_name')
        operation = self.request.query_params.get('operation')
        if medicine_name:
            queryset = queryset.filter(medicine__name__icontains=medicine_name)
        if operation:
            queryset = queryset.filter(operation=operation)
        return queryset.order_by('-created_at')
