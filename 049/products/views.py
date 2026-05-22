from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import ProductCategory, Product
from .serializers import ProductCategorySerializer, ProductSerializer
from inventory.models import Inventory
from inventory.services import InventoryService
from accounts.permissions import ProductManagePermission


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), ProductManagePermission()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if not serializer.validated_data.get('name'):
            raise ValidationError({'name': ['分类名称为必填项']})
        if ProductCategory.objects.filter(name=serializer.validated_data.get('name')).exists():
            raise ValidationError({'name': ['分类名称已存在']})
        serializer.save()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), ProductManagePermission()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        name = self.request.query_params.get('name')
        category_id = self.request.query_params.get('category')
        is_active = self.request.query_params.get('is_active')
        stock_status = self.request.query_params.get('stock_status')
        
        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(product_code__icontains=name))
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        
        if stock_status:
            product_ids = []
            for product in queryset:
                try:
                    inventory = Inventory.objects.get(product=product)
                    if stock_status == 'low' and inventory.is_low_stock:
                        product_ids.append(product.id)
                    elif stock_status == 'normal' and not inventory.is_low_stock:
                        product_ids.append(product.id)
                    elif stock_status == 'out' and inventory.quantity <= 0:
                        product_ids.append(product.id)
                except Inventory.DoesNotExist:
                    if stock_status == 'out':
                        product_ids.append(product.id)
            queryset = queryset.filter(id__in=product_ids)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        self.validate_product_data(serializer.validated_data)
        product = serializer.save()
        Inventory.objects.get_or_create(product=product, defaults={'quantity': 0})

    def perform_update(self, serializer):
        self.validate_product_data(serializer.validated_data)
        serializer.save()

    def validate_product_data(self, data):
        required_fields = ['product_code', 'name', 'category', 'purchase_price', 'wholesale_price', 'unit']
        missing_fields = [field for field in required_fields if field not in data or data[field] in [None, '']]
        if missing_fields:
            raise ValidationError({field: ['该字段为必填项'] for field in missing_fields})
        
        purchase_price = data.get('purchase_price')
        wholesale_price = data.get('wholesale_price')
        
        if purchase_price is not None and purchase_price < 0:
            raise ValidationError({'purchase_price': ['采购价格不能为负数']})
        
        if wholesale_price is not None and wholesale_price < 0:
            raise ValidationError({'wholesale_price': ['批发价格不能为负数']})
        
        if purchase_price is not None and wholesale_price is not None and wholesale_price < purchase_price:
            raise ValidationError({'wholesale_price': ['批发价格不能低于采购价格']})

    @action(detail=False, methods=['get'])
    def active_products(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
