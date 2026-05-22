from django.contrib import admin
from .models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'name', 'category', 'purchase_price', 'wholesale_price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['product_code', 'name']
