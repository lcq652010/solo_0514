from rest_framework import serializers
from .models import Student, Coach, Vehicle, Schedule, TrainingReservation, ExamRegistration, Payment, StudentArchive
import re
from django.utils import timezone


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['student_id', 'created_at', 'updated_at']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('姓名不能为空')
        if len(value) < 2 or len(value) > 20:
            raise serializers.ValidationError('姓名长度应在2-20个字符之间')
        return value

    def validate_id_card(self, value):
        value = value.strip()
        if not re.match(r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', value):
            raise serializers.ValidationError('身份证号格式不正确')
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'
        read_only_fields = ['coach_id', 'created_at', 'updated_at']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('姓名不能为空')
        if len(value) < 2 or len(value) > 20:
            raise serializers.ValidationError('姓名长度应在2-20个字符之间')
        return value

    def validate_id_card(self, value):
        value = value.strip()
        if not re.match(r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', value):
            raise serializers.ValidationError('身份证号格式不正确')
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError('教龄不能为负数')
        if value > 50:
            raise serializers.ValidationError('教龄不能超过50年')
        return value


class VehicleSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_plate_number(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('车牌号不能为空')
        if not re.match(r'^[\u4e00-\u9fa5][A-Z][A-Z0-9]{5}$', value):
            raise serializers.ValidationError('车牌号格式不正确')
        return value

    def validate_mileage(self, value):
        if value < 0:
            raise serializers.ValidationError('里程数不能为负数')
        return value


class ScheduleSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach.name', read_only=True)
    vehicle_plate = serializers.CharField(source='vehicle.plate_number', read_only=True)
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['current_students', 'created_at', 'updated_at']

    def get_available_slots(self, obj):
        return obj.max_students - obj.current_students

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError('结束时间必须晚于开始时间')

        if data['date'] < timezone.now().date():
            raise serializers.ValidationError('排班日期不能早于今天')

        if data['max_students'] <= 0:
            raise serializers.ValidationError('最大学员数必须大于0')

        if data['max_students'] > 10:
            raise serializers.ValidationError('最大学员数不能超过10人')

        return data


class TrainingReservationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    coach_name = serializers.CharField(source='schedule.coach.name', read_only=True)
    vehicle_plate = serializers.CharField(source='schedule.vehicle.plate_number', read_only=True)
    schedule_date = serializers.DateField(source='schedule.date', read_only=True)
    schedule_start_time = serializers.TimeField(source='schedule.start_time', read_only=True)
    schedule_end_time = serializers.TimeField(source='schedule.end_time', read_only=True)

    class Meta:
        model = TrainingReservation
        fields = '__all__'
        read_only_fields = ['reservation_time', 'created_at', 'updated_at',
                          'actual_start_time', 'actual_end_time']

    def validate(self, data):
        if 'subject' in data and not data['subject'].strip():
            raise serializers.ValidationError('培训科目不能为空')
        return data


class ExamRegistrationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)

    class Meta:
        model = ExamRegistration
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if 'exam_date' in data and data['exam_date'] < timezone.now().date():
            raise serializers.ValidationError('考试日期不能早于今天')

        if 'score' in data and data['score'] is not None:
            if data['score'] < 0 or data['score'] > 100:
                raise serializers.ValidationError('分数必须在0-100之间')

        return data


class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'payment_time']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('金额必须大于0')
        return value

    def validate_operator(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('经办人不能为空')
        return value


class StudentArchiveSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)

    class Meta:
        model = StudentArchive
        fields = '__all__'
        read_only_fields = ['archive_no', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    coach_name = serializers.CharField(source='coach.name', read_only=True, allow_null=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TrainingHoursSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    coach_name = serializers.CharField(source='coach.name', read_only=True)
    vehicle_plate = serializers.CharField(source='vehicle.plate_number', read_only=True)

    class Meta:
        model = TrainingHours
        fields = '__all__'
        read_only_fields = ['created_at']


class TrainingArchiveSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    remaining_hours = serializers.SerializerMethodField()

    class Meta:
        model = TrainingArchive
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_remaining_hours(self, obj):
        if obj.total_hours > 0:
            return float(obj.total_hours) - float(obj.completed_hours)
        return 0.0
