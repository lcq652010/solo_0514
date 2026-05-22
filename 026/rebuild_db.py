import os
from app import app, db

db_path = 'instance/orders.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print('旧数据库已删除')

with app.app_context():
    db.create_all()
    print('V2.0 数据库已创建完成')
    print('包含字段:')
    print('  - Order 表: pattern_complexity, calculated_price, estimated_days, estimated_delivery')
    print('  - Order 表: assigned_craftsman_id, assigned_craftsman_name')
    print('  - Craftsman 表完整字段')
