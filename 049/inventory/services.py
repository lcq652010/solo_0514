from django.db import transaction
from django.utils import timezone
from .models import Inventory, StockRecord, StockAlert
from accounts.models import StockAlertMessage


class InventoryService:
    @staticmethod
    @transaction.atomic
    def stock_in(product, quantity, related_order_no='', remark=''):
        inventory, created = Inventory.objects.get_or_create(
            product=product,
            defaults={'quantity': 0}
        )
        
        before_quantity = inventory.quantity
        inventory.quantity += quantity
        inventory.save()
        
        StockRecord.objects.create(
            product=product,
            record_type='in',
            quantity=quantity,
            before_quantity=before_quantity,
            after_quantity=inventory.quantity,
            related_order_no=related_order_no,
            remark=remark
        )
        
        StockAlert.objects.filter(product=product, is_handled=False).update(
            is_handled=True,
            handled_at=timezone.now()
        )
        
        return inventory

    @staticmethod
    @transaction.atomic
    def stock_out(product, quantity, related_order_no='', remark=''):
        try:
            inventory = Inventory.objects.get(product=product)
        except Inventory.DoesNotExist:
            raise ValueError(f'商品 {product.name} 库存记录不存在')
        
        if inventory.quantity < quantity:
            raise ValueError(f'商品 {product.name} 库存不足，当前库存：{inventory.quantity}')
        
        before_quantity = inventory.quantity
        inventory.quantity -= quantity
        inventory.save()
        
        StockRecord.objects.create(
            product=product,
            record_type='out',
            quantity=quantity,
            before_quantity=before_quantity,
            after_quantity=inventory.quantity,
            related_order_no=related_order_no,
            remark=remark
        )
        
        InventoryService.check_stock_alert(product, inventory)
        
        return inventory

    @staticmethod
    def check_stock_alert(product, inventory=None):
        if inventory is None:
            try:
                inventory = Inventory.objects.get(product=product)
            except Inventory.DoesNotExist:
                return
        
        alert_level = None
        message = ''
        
        if inventory.quantity <= 0:
            alert_level = 'danger'
            message = f'商品【{product.name}】库存已为空，请及时补货！'
        elif inventory.quantity <= product.min_stock * 0.5:
            alert_level = 'danger'
            message = f'商品【{product.name}】库存严重不足，当前库存：{inventory.quantity}，预警线：{product.min_stock}，请立即补货！'
        elif inventory.quantity < product.min_stock:
            alert_level = 'warning'
            message = f'商品【{product.name}】库存低于预警线，当前库存：{inventory.quantity}，预警线：{product.min_stock}，请及时补货。'
        
        if alert_level:
            StockAlert.objects.get_or_create(
                product=product,
                alert_type='low' if alert_level == 'warning' else 'low',
                is_handled=False,
                defaults={
                    'current_quantity': inventory.quantity,
                    'min_stock': product.min_stock
                }
            )
            
            StockAlertMessage.objects.create(
                product=product,
                alert_level=alert_level,
                current_quantity=inventory.quantity,
                min_stock=product.min_stock,
                message=message
            )
        
        return {
            'has_alert': alert_level is not None,
            'alert_level': alert_level,
            'message': message
        }

    @staticmethod
    def batch_check_stock_alerts():
        alerts = []
        for inventory in Inventory.objects.all():
            result = InventoryService.check_stock_alert(inventory.product, inventory)
            if result['has_alert']:
                alerts.append({
                    'product': inventory.product,
                    'inventory': inventory,
                    **result
                })
        return alerts

    @staticmethod
    def get_stock_status(product):
        try:
            inventory = Inventory.objects.get(product=product)
            if inventory.quantity <= 0:
                return 'out'
            elif inventory.quantity < product.min_stock:
                return 'low'
            else:
                return 'normal'
        except Inventory.DoesNotExist:
            return 'out'
