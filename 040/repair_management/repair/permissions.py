from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'admin'


class IsReception(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'reception'


class IsEngineer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'engineer'


class IsAdminOrReception(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role in ['admin', 'reception']


class IsAdminOrEngineer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role in ['admin', 'engineer']


class IsOwnerOrAssignedEngineer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.profile.role == 'admin':
            return True
        if hasattr(obj, 'assigned_to') and obj.assigned_to == request.user:
            return True
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        return False


class RepairOrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.profile.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.profile.role == 'reception':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH']
        
        if request.user.profile.role == 'engineer':
            return request.method in ['GET', 'PUT', 'PATCH']
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.profile.role == 'admin':
            return True
        
        if request.user.profile.role == 'reception':
            return True
        
        if request.user.profile.role == 'engineer':
            return obj.assigned_to == request.user
        
        return False
