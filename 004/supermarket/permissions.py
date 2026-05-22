from rest_framework.permissions import BasePermission, IsAuthenticated


class IsCashier(BasePermission):
    """收银员权限"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_cashier or request.user.is_admin)


class IsWarehouse(BasePermission):
    """库管员权限"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_warehouse or request.user.is_admin)


class IsAdmin(BasePermission):
    """管理员权限"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsCashierOrWarehouse(BasePermission):
    """收银员或库管员权限"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_cashier or request.user.is_warehouse or request.user.is_admin
        )


# 权限矩阵说明:
# | 功能/模块   | 收银员 | 库管员 | 管理员 |
# |------------|--------|--------|--------|
# | 商品查看   |   ✓    |   ✓    |   ✓    |
# | 商品管理   |        |        |   ✓    |
# | 库存调整   |        |   ✓    |   ✓    |
# | 采购入库   |        |   ✓    |   ✓    |
# | 收银结账   |   ✓    |        |   ✓    |
# | 订单退款   |   ✓    |        |   ✓    |
# | 会员管理   |   ✓    |        |   ✓    |
# | 查看日志   |        |   ✓    |   ✓    |
# | 用户管理   |        |        |   ✓    |
