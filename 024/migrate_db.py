import sqlite3
import os

DATABASE = 'traffic_management.db'

def migrate_database():
    if not os.path.exists(DATABASE):
        print("数据库不存在，将在首次运行时自动创建")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        print("开始迁移数据库...")
        
        cursor.execute("PRAGMA table_info(devices)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'device_model' not in columns:
            print("添加设备型号字段...")
            cursor.execute('ALTER TABLE devices ADD COLUMN device_model TEXT')
        
        if 'communication_protocol' not in columns:
            print("添加通信协议字段...")
            cursor.execute('ALTER TABLE devices ADD COLUMN communication_protocol TEXT')
        
        if 'enable_date' not in columns:
            print("添加启用日期字段...")
            cursor.execute('ALTER TABLE devices ADD COLUMN enable_date TEXT')
        
        if 'service_hall' not in columns:
            print("添加服务大厅字段...")
            cursor.execute('ALTER TABLE devices ADD COLUMN service_hall TEXT')
        
        cursor.execute("PRAGMA table_info(work_orders)")
        wo_columns = [col[1] for col in cursor.fetchall()]
        
        if 'fault_category' not in wo_columns:
            print("添加故障分类字段...")
            cursor.execute('ALTER TABLE work_orders ADD COLUMN fault_category TEXT NOT NULL DEFAULT "其他"')
        
        if 'fault_level' not in wo_columns:
            print("添加故障等级字段...")
            cursor.execute('ALTER TABLE work_orders ADD COLUMN fault_level TEXT NOT NULL DEFAULT "一般"')
        
        if 'priority' not in wo_columns:
            print("添加优先级字段...")
            cursor.execute('ALTER TABLE work_orders ADD COLUMN priority TEXT NOT NULL DEFAULT "中"')
        
        conn.commit()
        print("数据库迁移完成！")
        
    except Exception as e:
        print(f"迁移过程出错: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
