import sqlite3
import os

DATABASE_PATH = 'container_terminal.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_code TEXT UNIQUE NOT NULL,
            device_name TEXT NOT NULL,
            device_type TEXT NOT NULL,
            device_model TEXT,
            protection_level TEXT,
            serial_number TEXT,
            commission_date TEXT,
            harbor_area TEXT,
            work_area TEXT,
            location TEXT NOT NULL,
            install_date TEXT NOT NULL,
            status TEXT DEFAULT '正常',
            is_online INTEGER DEFAULT 1,
            last_online_time TEXT DEFAULT CURRENT_TIMESTAMP,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP,
            update_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE work_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE NOT NULL,
            device_id INTEGER NOT NULL,
            fault_type TEXT NOT NULL,
            fault_level TEXT DEFAULT '一般',
            priority TEXT DEFAULT '一般',
            fault_description TEXT NOT NULL,
            reporter TEXT NOT NULL,
            report_time TEXT NOT NULL,
            status TEXT DEFAULT '待处理',
            handler TEXT,
            handle_time TEXT,
            handle_duration INTEGER,
            handle_result TEXT,
            before_status TEXT,
            after_status TEXT,
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE maintenance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT NOT NULL,
            device_id INTEGER NOT NULL,
            device_name TEXT NOT NULL,
            device_code TEXT NOT NULL,
            harbor_area TEXT,
            work_area TEXT,
            fault_type TEXT NOT NULL,
            fault_level TEXT NOT NULL,
            priority TEXT NOT NULL,
            fault_description TEXT NOT NULL,
            reporter TEXT NOT NULL,
            report_time TEXT NOT NULL,
            handler TEXT NOT NULL,
            handle_time TEXT NOT NULL,
            handle_duration INTEGER,
            handle_result TEXT NOT NULL,
            before_status TEXT,
            after_status TEXT,
            cost REAL DEFAULT 0,
            remark TEXT,
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    ''')

    cursor.execute('''
        CREATE TRIGGER update_device_update_time 
        AFTER UPDATE ON devices
        FOR EACH ROW
        BEGIN
            UPDATE devices SET update_time = CURRENT_TIMESTAMP WHERE id = OLD.id;
        END;
    ''')

    conn.commit()
    conn.close()
    print("数据库初始化完成！")

def generate_order_no():
    from datetime import datetime
    conn = get_db_connection()
    cursor = conn.cursor()
    
    date_prefix = datetime.now().strftime('%Y%m%d')
    
    cursor.execute('''
        SELECT order_no FROM work_orders 
        WHERE order_no LIKE ? 
        ORDER BY order_no DESC LIMIT 1
    ''', (f'WO{date_prefix}%',))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        last_no = result['order_no']
        sequence = int(last_no[-4:]) + 1
    else:
        sequence = 1
    
    return f'WO{date_prefix}{sequence:04d}'

HARBOR_AREAS = ['港区A', '港区B', '港区C', '港区D']
WORK_AREAS = ['集装箱堆场', '码头作业区', '闸口通道', '海关查验区', '冷藏箱区']
FAULT_LEVELS = ['轻微', '一般', '严重', '致命']

if __name__ == '__main__':
    init_db()
