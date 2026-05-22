import os
from app import app, db

def init_db():
    os.makedirs('instance', exist_ok=True)
    with app.app_context():
        db.create_all()
        print("数据库初始化完成！")

if __name__ == '__main__':
    init_db()