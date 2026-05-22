from app import db
from datetime import datetime, timedelta
import re

ORDER_STATUS = [
    '待接单',
    '制胎',
    '施釉',
    '绘彩',
    '烧造',
    '打磨',
    '镶口',
    '完工'
]

BODY_MATERIALS = [
    '紫铜胎',
    '黄铜胎',
    '白银胎',
    '金胎',
    '瓷胎',
    '玻璃胎',
    '木胎',
    '其他'
]

BOTTLE_STYLES = [
    '扁壶形',
    '圆形',
    '方形',
    '六方形',
    '八方形',
    '瓜棱形',
    '海棠形',
    '马蹄形',
    '荷包形',
    '其他'
]

DECORATIVE_PATTERNS = [
    '山水纹饰',
    '花鸟纹饰',
    '人物故事',
    '吉祥图案',
    '龙凤纹饰',
    '缠枝花卉',
    '博古纹饰',
    '西洋纹饰',
    '书法题字',
    '定制图案'
]

ENAMEL_COLORS = [
    '故宫红',
    '宝石蓝',
    '翡翠绿',
    '明黄',
    '葡萄紫',
    '胭脂粉',
    '月白',
    '牙白',
    '墨色',
    '鎏金',
    '多彩混搭'
]

COMPLEXITY_LEVELS = ['简单', '中等', '复杂', '极复杂']

CRAFTSMEN = [
    {'id': 1, 'name': '张铜匠', 'specialty': '制胎', 'skill_level': '大师', 'price_factor': 1.5},
    {'id': 2, 'name': '李釉工', 'specialty': '施釉', 'skill_level': '高级', 'price_factor': 1.2},
    {'id': 3, 'name': '王画师', 'specialty': '绘彩', 'skill_level': '大师', 'price_factor': 1.8},
    {'id': 4, 'name': '赵窑师', 'specialty': '烧造', 'skill_level': '高级', 'price_factor': 1.3},
    {'id': 5, 'name': '陈巧匠', 'specialty': '综合', 'skill_level': '资深', 'price_factor': 1.4}
]

MATERIAL_BASE_PRICE = {
    '紫铜胎': 800,
    '黄铜胎': 500,
    '白银胎': 3000,
    '金胎': 15000,
    '瓷胎': 300,
    '玻璃胎': 200,
    '木胎': 150,
    '其他': 400
}

COMPLEXITY_PRICE_FACTOR = {
    '简单': 1.0,
    '中等': 1.5,
    '复杂': 2.5,
    '极复杂': 4.0
}

COLOR_COUNT_FACTOR = {1: 1.0, 2: 1.2, 3: 1.4, 4: 1.6, 5: 1.8, 'more': 2.0}

PROCESS_DAYS = {
    '制胎': 3,
    '施釉': 2,
    '绘彩': {'简单': 3, '中等': 5, '复杂': 8, '极复杂': 12},
    '烧造': 2,
    '打磨': 1,
    '镶口': 1
}

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(50), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.String(200))
    
    bottle_style = db.Column(db.String(50))
    bottle_dimensions = db.Column(db.String(100))
    body_material = db.Column(db.String(50), nullable=False)
    
    decorative_pattern = db.Column(db.String(100), nullable=False)
    pattern_detail = db.Column(db.Text)
    enamel_color_system = db.Column(db.String(200), nullable=False)
    complexity = db.Column(db.String(20), default='中等')
    
    glaze_requirement = db.Column(db.Text)
    painting_detail = db.Column(db.Text)
    firing_requirement = db.Column(db.Text)
    
    craftsman_id = db.Column(db.Integer)
    craftsman_name = db.Column(db.String(50))
    estimated_days = db.Column(db.Integer)
    estimated_delivery = db.Column(db.DateTime)
    actual_delivery = db.Column(db.DateTime)
    
    special_requirement = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)
    base_price = db.Column(db.Float)
    material_price = db.Column(db.Float)
    complexity_price = db.Column(db.Float)
    color_price = db.Column(db.Float)
    craftsman_price = db.Column(db.Float)
    estimated_price = db.Column(db.Float)
    
    status = db.Column(db.String(20), nullable=False, default='待接单')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    remarks = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_address': self.customer_address,
            'bottle_style': self.bottle_style,
            'bottle_dimensions': self.bottle_dimensions,
            'body_material': self.body_material,
            'decorative_pattern': self.decorative_pattern,
            'pattern_detail': self.pattern_detail,
            'enamel_color_system': self.enamel_color_system,
            'complexity': self.complexity,
            'glaze_requirement': self.glaze_requirement,
            'painting_detail': self.painting_detail,
            'firing_requirement': self.firing_requirement,
            'craftsman_id': self.craftsman_id,
            'craftsman_name': self.craftsman_name,
            'estimated_days': self.estimated_days,
            'estimated_delivery': self.estimated_delivery.strftime('%Y-%m-%d') if self.estimated_delivery else None,
            'actual_delivery': self.actual_delivery.strftime('%Y-%m-%d') if self.actual_delivery else None,
            'special_requirement': self.special_requirement,
            'quantity': self.quantity,
            'base_price': self.base_price,
            'material_price': self.material_price,
            'complexity_price': self.complexity_price,
            'color_price': self.color_price,
            'craftsman_price': self.craftsman_price,
            'estimated_price': self.estimated_price,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'remarks': self.remarks
        }

def generate_order_no():
    last_order = Order.query.order_by(Order.id.desc()).first()
    today = datetime.now()
    prefix = f"ENB{today.strftime('%Y%m%d')}"
    if last_order and last_order.order_no.startswith(prefix):
        match = re.search(r'(\d{4})$', last_order.order_no)
        if match:
            seq = int(match.group(1)) + 1
        else:
            seq = 1
    else:
        seq = 1
    return f"{prefix}{seq:04d}"


def calculate_price(body_material, complexity, enamel_color_system, quantity=1, craftsman_factor=1.0):
    base_price = 1000
    material_price = MATERIAL_BASE_PRICE.get(body_material, 400)
    complexity_factor = COMPLEXITY_PRICE_FACTOR.get(complexity, 1.5)
    complexity_price = base_price * complexity_factor
    
    color_count = len([c for c in ['、', ',', '，', '/'] if c in enamel_color_system]) + 1
    if color_count > 5:
        color_factor = COLOR_COUNT_FACTOR['more']
    else:
        color_factor = COLOR_COUNT_FACTOR.get(color_count, 1.0)
    color_price = base_price * (color_factor - 1)
    
    craftsman_price = base_price * (craftsman_factor - 1) if craftsman_factor > 1 else 0
    
    unit_price = base_price + material_price + complexity_price + color_price + craftsman_price
    total_price = unit_price * quantity
    
    return {
        'base_price': base_price,
        'material_price': material_price,
        'complexity_price': complexity_price,
        'color_price': color_price,
        'craftsman_price': craftsman_price,
        'estimated_price': total_price
    }


def calculate_days(complexity):
    total_days = PROCESS_DAYS['制胎'] + PROCESS_DAYS['施釉'] + PROCESS_DAYS['烧造'] + PROCESS_DAYS['打磨'] + PROCESS_DAYS['镶口']
    painting_days = PROCESS_DAYS['绘彩'].get(complexity, PROCESS_DAYS['绘彩']['中等'])
    total_days += painting_days
    return total_days


def estimate_delivery_date(start_date=None, complexity='中等'):
    if start_date is None:
        start_date = datetime.now()
    days = calculate_days(complexity)
    return start_date + timedelta(days=days)


def get_craftsman_by_id(craftsman_id):
    for craftsman in CRAFTSMEN:
        if craftsman['id'] == craftsman_id:
            return craftsman
    return None


def validate_order_data(data):
    errors = []
    
    required_fields = ['customer_name', 'customer_phone', 'body_material', 'decorative_pattern', 'enamel_color_system']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f'缺少必填字段: {field}')
    
    if 'customer_phone' in data and data['customer_phone']:
        if not re.match(r'^1[3-9]\d{9}$', data['customer_phone']):
            errors.append('手机号码格式不正确')
    
    if 'body_material' in data and data['body_material'] not in BODY_MATERIALS:
        errors.append(f'胎体材质无效，可选值: {", ".join(BODY_MATERIALS)}')
    
    if 'decorative_pattern' in data and data['decorative_pattern'] not in DECORATIVE_PATTERNS:
        errors.append(f'纹饰图案无效，可选值: {", ".join(DECORATIVE_PATTERNS)}')
    
    if 'complexity' in data and data['complexity'] not in COMPLEXITY_LEVELS:
        errors.append(f'复杂度级别无效，可选值: {", ".join(COMPLEXITY_LEVELS)}')
    
    if 'quantity' in data:
        try:
            qty = int(data['quantity'])
            if qty < 1 or qty > 100:
                errors.append('数量必须在1-100之间')
        except (ValueError, TypeError):
            errors.append('数量必须是有效数字')
    
    return errors