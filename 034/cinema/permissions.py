from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='管理员').exists()

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='售票员').exists() or
            request.user.groups.filter(name='管理员').exists()
        )

class IsChecker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='检票员').exists() or
            request.user.groups.filter(name='管理员').exists()
        )

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='管理员').exists()

class MoviePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='管理员').exists()

class HallPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='管理员').exists()

class SchedulePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='管理员').exists()

class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if view.action == 'create':
            return request.user.groups.filter(name__in=['售票员', '管理员']).exists()
        
        if view.action in ['refund', 'partial_update', 'update']:
            return request.user.groups.filter(name__in=['售票员', '管理员']).exists()
        
        return request.user.groups.filter(name='管理员').exists()

class SeatPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='管理员').exists()
