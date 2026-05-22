from rest_framework.permissions import BasePermission


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'profile') and request.user.profile.role in ['receptionist', 'admin']


class IsHousekeeper(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'profile') and request.user.profile.role in ['housekeeper', 'admin']


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'profile') and request.user.profile.role == 'admin'


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS']


def get_user_role(user):
    if user.is_superuser:
        return 'admin'
    if hasattr(user, 'profile'):
        return user.profile.role
    return None
