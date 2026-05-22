from rest_framework import serializers
from .models import (
    Student, Coach, Vehicle, CoachSchedule, TrainingAppointment, 
    TrainingRecord, FeeSettlement, SubjectHourConfig, StudentSubjectStats
)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class VehicleSerializer(serializers.ModelSerializer):
    current_coach_name = serializers.CharField(source='current_coach.name', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CoachScheduleSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach.name', read_only=True)
    
    class Meta:
        model = CoachSchedule
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class TrainingAppointmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    coach_name = serializers.CharField(source='coach.name', read_only=True)
    vehicle_plate = serializers.CharField(source='vehicle.plate_number', read_only=True)
    
    class Meta:
        model = TrainingAppointment
        fields = '__all__'
        read_only_fields = ['id', 'appointment_number', 'created_at', 'updated_at']


class TrainingRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    coach_name = serializers.CharField(source='coach.name', read_only=True)
    vehicle_plate = serializers.CharField(source='vehicle.plate_number', read_only=True)
    appointment_number = serializers.CharField(source='appointment.appointment_number', read_only=True)
    
    class Meta:
        model = TrainingRecord
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'training_hours', 'effective_hours', 'exceeded_hours']


class FeeSettlementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = FeeSettlement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubjectHourConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectHourConfig
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentSubjectStatsSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentSubjectStats
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'can_schedule_exam']
    
    def get_progress_percentage(self, obj):
        if obj.required_hours > 0:
            return round((obj.total_effective_hours / obj.required_hours) * 100, 2)
        return 0
