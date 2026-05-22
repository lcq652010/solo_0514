from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import PermissionDenied


def get_user_role(user):
    if not user.is_authenticated:
        return None
    try:
        return user.userprofile.role
    except:
        return None


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = get_user_role(request.user)
        return role == 'admin' or request.user.is_staff


class IsPhotographer(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = get_user_role(request.user)
        return role in ['photographer', 'admin']


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = get_user_role(request.user)
        return role in ['customer', 'photographer', 'admin']


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        role = get_user_role(request.user)
        if role == 'admin':
            return True
        if hasattr(obj, 'customer') and hasattr(obj.customer, 'user'):
            return obj.customer.user == request.user
        if hasattr(obj, 'photographer') and hasattr(obj.photographer, 'user'):
            return obj.photographer.user == request.user
        return False


class IsPhotographerOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        role = get_user_role(request.user)
        if role == 'admin':
            return True
        if hasattr(obj, 'photographer') and hasattr(obj.photographer, 'user'):
            return obj.photographer.user == request.user
        return False


class IsCustomerOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        role = get_user_role(request.user)
        if role == 'admin':
            return True
        if hasattr(obj, 'customer') and hasattr(obj.customer, 'user'):
            return obj.customer.user == request.user
        return False
