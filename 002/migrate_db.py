import sqlite3
import os
import shutil
from datetime import datetime

DATABASE_PATH = 'container_terminal.db'
BACKUP_PATH = f'container_terminal_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'

def backup_database():
    if os.path.exists(DATABASE_PATH):
        shutil.copy2(DATABASE_PATH, BACKUP_PATH)
        print(f"数据库已备份到: {BACKUP_PATH}")
        return True
    return False

def migrate_v1_to_v3():
    if not os.path.exists(DATABASE_PATH):
        print("数据库不存在，执行初始化...")
        from database import init_db
        init_db()
        return

    backup_database()
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        print("开始迁移设备表...")
        cursor.execute("PRAGMA table_info(devices)")
        columns = [col[1] for col in cursor.fetchall()]
        
        new_fields = ['harbor_area', 'work_area', 'is_online', 'last_online_time']
        for field in new_fields:
            if field not in columns:
                cursor.execute(f"ALTER TABLE devices ADD COLUMN {field} TEXT")
                print(f"  - 添加 {field} 字段")
        
        cursor.execute("UPDATE devices SET is_online = 1 WHERE is_online IS NULL")
        conn.commit()
        
        print("迁移工单表...")
        cursor.execute("PRAGMA table_info(work_orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        new_fields = ['fault_level', 'handle_duration', 'before_status', 'after_status']
        for field in new_fields:
            if field not in columns:
                cursor.execute(f"ALTER TABLE work_orders ADD COLUMN {field} TEXT")
                print(f"  - 添加 {field} 字段")
        
        conn.commit()
        
        print("迁移运维记录表...")
        cursor.execute("PRAGMA table_info(maintenance_records)")
        columns = [col[1] for col in cursor.fetchall()]
        
        new_fields = ['device_code', 'harbor_area', 'work_area', 'fault_level', 
                      'reporter', 'report_time', 'handle_duration', 'before_status', 'after_status']
        for field in new_fields:
            if field not in columns:
                cursor.execute(f"ALTER TABLE maintenance_records ADD COLUMN {field} TEXT")
                print(f"  - 添加 {field} 字段")
        
        conn.commit()
        
        print("\n数据库迁移完成！")
        
    except Exception as e:
        conn.rollback()
        print(f"迁移失败: {e}")
        if os.path.exists(BACKUP_PATH):
            shutil.copy2(BACKUP_PATH, DATABASE_PATH)
            print("已从备份恢复数据库")
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_v1_to_v3()
