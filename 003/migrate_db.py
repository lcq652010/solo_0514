import os
import sqlite3
from app import app, db

db_path = os.path.join(app.root_path, 'baggage_management.db')

def migrate_database():
    print('开始数据库迁移 v3.0...')
    
    if os.path.exists(db_path):
        print(f'找到现有数据库: {db_path}')
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("PRAGMA table_info(devices)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'device_model' not in columns:
                print('添加 device_model 字段...')
                cursor.execute('ALTER TABLE devices ADD COLUMN device_model VARCHAR(100)')
            
            if 'communication_mode' not in columns:
                print('添加 communication_mode 字段...')
                cursor.execute('ALTER TABLE devices ADD COLUMN communication_mode VARCHAR(50)')
            
            if 'activation_date' not in columns:
                print('添加 activation_date 字段...')
                cursor.execute('ALTER TABLE devices ADD COLUMN activation_date DATE')
            
            if 'terminal' not in columns:
                print('添加 terminal 字段...')
                cursor.execute('ALTER TABLE devices ADD COLUMN terminal VARCHAR(50)')
            
            if 'checkin_island' not in columns:
                print('添加 checkin_island 字段...')
                cursor.execute('ALTER TABLE devices ADD COLUMN checkin_island VARCHAR(50)')
            
            cursor.execute("PRAGMA table_info(work_orders)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'fault_type' not in columns:
                print('添加 fault_type 字段...')
                cursor.execute('ALTER TABLE work_orders ADD COLUMN fault_type VARCHAR(50) NOT NULL DEFAULT "其他"')
            
            if 'priority' not in columns:
                print('添加 priority 字段...')
                cursor.execute('ALTER TABLE work_orders ADD COLUMN priority VARCHAR(20) NOT NULL DEFAULT "普通"')
            
            if 'fault_level' not in columns:
                print('添加 fault_level 字段...')
                cursor.execute('ALTER TABLE work_orders ADD COLUMN fault_level VARCHAR(20) NOT NULL DEFAULT "一般"')
            
            if 'repair_duration' not in columns:
                print('添加 repair_duration 字段...')
                cursor.execute('ALTER TABLE work_orders ADD COLUMN repair_duration INTEGER')
            
            if 'parts_used' not in columns:
                print('添加 parts_used 字段...')
                cursor.execute('ALTER TABLE work_orders ADD COLUMN parts_used TEXT')
            
            cursor.execute("PRAGMA table_info(maintenance_records)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'work_order_no' not in columns:
                print('添加 work_order_no 字段...')
                cursor.execute('ALTER TABLE maintenance_records ADD COLUMN work_order_no VARCHAR(50)')
            
            if 'fault_type' not in columns:
                print('添加 fault_type 字段到 maintenance_records...')
                cursor.execute('ALTER TABLE maintenance_records ADD COLUMN fault_type VARCHAR(50)')
            
            if 'fault_level' not in columns:
                print('添加 fault_level 字段到 maintenance_records...')
                cursor.execute('ALTER TABLE maintenance_records ADD COLUMN fault_level VARCHAR(20)')
            
            if 'duration' not in columns:
                print('添加 duration 字段...')
                cursor.execute('ALTER TABLE maintenance_records ADD COLUMN duration INTEGER')
            
            if 'parts_used' not in columns:
                print('添加 parts_used 字段到 maintenance_records...')
                cursor.execute('ALTER TABLE maintenance_records ADD COLUMN parts_used TEXT')
            
            conn.commit()
            print('数据库 v3.0 迁移完成！')
            
        except Exception as e:
            print(f'迁移过程中出错: {e}')
            conn.rollback()
        finally:
            conn.close()
    else:
        print('未找到现有数据库，将创建新数据库。')
        with app.app_context():
            db.create_all()
        print('新数据库创建完成！')

if __name__ == '__main__':
    migrate_database()
