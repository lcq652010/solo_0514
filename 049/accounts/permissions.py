from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Permission, UserProfile


class RolePermission(BasePermission):
    required_permission = None

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        try:
            profile = UserProfile.objects.get(user=request.user)
            return Permission.has_permission(profile.role, self.required_permission)
        except UserProfile.DoesNotExist:
            return False


def has_permission(permission):
    def decorator(view_func):
        def wrapped(view, request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied('请先登录')
            
            if request.user.is_superuser:
                return view_func(view, request, *args, **kwargs)
            
            try:
                profile = UserProfile.objects.get(user=request.user)
                if not Permission.has_permission(profile.role, permission):
                    raise PermissionDenied('您没有该操作权限')
            except UserProfile.DoesNotExist:
                raise PermissionDenied('用户信息不存在')
            
            return view_func(view, request, *args, **kwargs)
        return wrapped
    return decorator


class OrderManagePermission(RolePermission):
    required_permission = Permission.ORDER_MANAGE


class WarehouseManagePermission(RolePermission):
    required_permission = Permission.WAREHOUSE_MANAGE


class ViewReportsPermission(RolePermission):
    required_permission = Permission.VIEW_REPORTS


class UserManagePermission(RolePermission):
    required_permission = Permission.USER_MANAGE


class ProductManagePermission(RolePermission):
    required_permission = Permission.PRODUCT_MANAGE


class SupplierManagePermission(RolePermission):
    required_permission = Permission.SUPPLIER_MANAGE


class CustomerManagePermission(RolePermission):
    required_permission = Permission.CUSTOMER_MANAGE


class SettlementManagePermission(RolePermission):
    required_permission = Permission.SETTLEMENT_MANAGE
