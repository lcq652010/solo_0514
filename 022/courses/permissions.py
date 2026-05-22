from rest_framework import permissions
from django.contrib.auth.models import User


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_student


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_instructor


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_admin


class IsInstructorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
            return False
        return request.user.profile.is_instructor or request.user.profile.is_admin


class IsCourseInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
            return False
        if request.user.profile.is_admin:
            return True
        return hasattr(obj, 'instructor') and obj.instructor == request.user


class IsEnrolledStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        from .models import Enrollment
        return Enrollment.objects.filter(user=request.user, course=obj).exists()


class IsOwnOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'profile') and request.user.profile.is_admin:
            return True
        return obj.user == request.user


class IsOwnEnrollment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'profile') and request.user.profile.is_admin:
            return True
        return obj.user == request.user


class IsInstructorOfCourse(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
            return False
        if request.user.profile.is_admin:
            return True
        course = obj.course if hasattr(obj, 'course') else obj
        return course.instructor == request.user


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
