import sqlite3
import os

DATABASE = 'gas_station.db'

def migrate():
    if not os.path.exists(DATABASE):
        print('数据库不存在，将在首次运行时自动创建')
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(devices)")
    columns = [col[1] for col in cursor.fetchall()]
    
    new_columns = [
        ('device_model', 'TEXT'),
        ('control_version', 'TEXT'),
        ('enable_date', 'TEXT'),
        ('station_area', 'TEXT'),
        ('gasoline_type', 'TEXT')
    ]
    
    for col_name, col_type in new_columns:
        if col_name not in columns:
            print(f'添加字段: {col_name}')
            cursor.execute(f'ALTER TABLE devices ADD COLUMN {col_name} {col_type}')
    
    cursor.execute("PRAGMA table_info(fault_reports)")
    columns = [col[1] for col in cursor.fetchall()]
    
    new_fault_columns = [
        ('fault_category', 'TEXT'),
        ('priority', 'TEXT DEFAULT \'normal\'')
    ]
    
    for col_name, col_type in new_fault_columns:
        if col_name not in columns:
            print(f'添加字段: {col_name}')
            cursor.execute(f'ALTER TABLE fault_reports ADD COLUMN {col_name} {col_type}')
    
    cursor.execute("PRAGMA table_info(maintenance_records)")
    columns = [col[1] for col in cursor.fetchall()]
    
    new_maint_columns = [
        ('fault_report_id', 'INTEGER'),
        ('action_taken', 'TEXT'),
        ('parts_replaced', 'TEXT')
    ]
    
    for col_name, col_type in new_maint_columns:
        if col_name not in columns:
            print(f'添加字段: {col_name}')
            cursor.execute(f'ALTER TABLE maintenance_records ADD COLUMN {col_name} {col_type}')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maintenance_id INTEGER NOT NULL,
            log_type TEXT NOT NULL,
            log_content TEXT NOT NULL,
            operator TEXT,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (maintenance_id) REFERENCES maintenance_records (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print('数据库迁移完成！')

if __name__ == '__main__':
    migrate()
