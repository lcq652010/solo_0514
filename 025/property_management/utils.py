from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions


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
        if hasattr(obj, 'owner') and hasattr(obj.owner, 'user'):
            return obj.owner.user == request.user
        return False


class IsWorkerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'worker') and hasattr(obj.worker, 'user'):
            return obj.worker.user == request.user
        return False


class IsOwnerWorkerAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'owner') and hasattr(obj.owner, 'user'):
            if obj.owner.user == request.user:
                return True
        if hasattr(obj, 'worker') and hasattr(obj.worker, 'user'):
            if obj.worker.user == request.user:
                return True
        return False


def get_user_role(user):
    if user.is_superuser:
        return 'super_admin'
    if user.is_staff:
        return 'admin'
    if hasattr(user, 'repairworker') and hasattr(user.repairworker, 'id'):
        return 'worker'
    if hasattr(user, 'owner') and hasattr(user.owner, 'id'):
        return 'owner'
    return 'user'
