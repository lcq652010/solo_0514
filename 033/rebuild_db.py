import os
import sys
print("当前目录:", os.getcwd())
print("脚本目录:", os.path.dirname(os.path.abspath(__file__)))

from app import app, db

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'water_meter.db')
print("数据库路径:", db_path)

if os.path.exists(db_path):
    os.remove(db_path)
    print("已删除旧数据库")
else:
    print("数据库文件不存在，将创建新库")

with app.app_context():
    db.create_all()
    print("数据库表创建成功！")