from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCashier(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'cashier' or request.user.role == 'admin'


class IsMaker(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'maker' or request.user.role == 'admin'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'


class CashierPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.user.role == 'cashier':
            if view.action in ['list', 'retrieve', 'create', 'pay', 'verify', 'detail_by_no']:
                return True
            if request.method in SAFE_METHODS:
                return True
            return False
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'cashier':
            return True
        return False


class MakerPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.user.role == 'maker':
            if view.action in ['list', 'retrieve', 'update_status', 'queue']:
                return True
            if request.method in SAFE_METHODS:
                return True
            return False
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'maker':
            return True
        return False


class ProductPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in SAFE_METHODS:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.method in SAFE_METHODS:
            return True
        return False


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in SAFE_METHODS:
            return True
        
        return False
