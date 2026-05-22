from rest_framework import permissions


class IsReceptionist(permissions.BasePermission):
    """
    前台权限
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.staff.role == 'receptionist'
        except:
            return False


class IsDoctor(permissions.BasePermission):
    """
    医生权限
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.staff.role == 'doctor'
        except:
            return False


class IsAdmin(permissions.BasePermission):
    """
    管理员权限
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.staff.role == 'admin'
        except:
            return False


class IsReceptionistOrDoctor(permissions.BasePermission):
    """
    前台或医生权限
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.staff.role in ['receptionist', 'doctor']
        except:
            return False


class IsDoctorOrAdmin(permissions.BasePermission):
    """
    医生或管理员权限
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.staff.role in ['doctor', 'admin']
        except:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    仅医生可以编辑自己的就诊记录
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        try:
            return hasattr(obj, 'doctor') and obj.doctor.staff and obj.doctor.staff.user == request.user
        except:
            return False
