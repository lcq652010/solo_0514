import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'water_meter.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print("已删除旧数据库")

from app import app, db

with app.app_context():
    db.create_all()
    print("数据库表创建成功！")

print("启动Flask服务器...")
app.run(debug=True, host='0.0.0.0', port=5000)