import sqlite3
import os
from datetime import datetime

DATABASE = 'gas_station.db'

FAULT_CATEGORIES = [
    'hardware',
    'software',
    'network',
    'power',
    'mechanical',
    'sensor',
    'other'
]

FAULT_CATEGORY_NAMES = {
    'hardware': '硬件故障',
    'software': '软件故障',
    'network': '网络故障',
    'power': '电源故障',
    'mechanical': '机械故障',
    'sensor': '传感器故障',
    'other': '其他故障'
}

PRIORITY_LEVELS = ['low', 'normal', 'high', 'urgent']

PRIORITY_NAMES = {
    'low': '低',
    'normal': '普通',
    'high': '高',
    'urgent': '紧急'
}

IMPACT_DESCRIPTIONS = {
    'low': '不影响正常运营，可择机处理',
    'normal': '影响较小，可安排当日处理',
    'high': '影响单台设备运营，需尽快处理',
    'urgent': '严重影响加油站运营，需立即处理'
}

PRIORITY_COLORS = {
    'low': '#28a745',
    'normal': '#17a2b8',
    'high': '#ffc107',
    'urgent': '#dc3545'
}

GASOLINE_TYPES = ['92#', '95#', '98#', '0#柴油', '其他']

STATION_AREAS = ['A区', 'B区', 'C区', 'D区', '东区', '西区', '南区', '北区', '其他']

MAINTENANCE_ACTIONS = ['检查', '维修', '更换配件', '校准', '清洁', '升级', '其他']

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_no TEXT UNIQUE NOT NULL,
            device_name TEXT NOT NULL,
            device_type TEXT NOT NULL,
            device_model TEXT,
            control_version TEXT,
            station_area TEXT,
            gasoline_type TEXT,
            location TEXT NOT NULL,
            status TEXT DEFAULT 'normal',
            install_date TEXT,
            enable_date TEXT,
            description TEXT,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP,
            update_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fault_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE NOT NULL,
            device_id INTEGER NOT NULL,
            fault_type TEXT NOT NULL,
            fault_category TEXT,
            priority TEXT DEFAULT 'normal',
            fault_description TEXT NOT NULL,
            reporter TEXT NOT NULL,
            contact TEXT,
            status TEXT DEFAULT 'pending',
            report_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT NOT NULL,
            device_id INTEGER NOT NULL,
            fault_report_id INTEGER,
            maintenance_type TEXT NOT NULL,
            maintenance_content TEXT NOT NULL,
            maintenance_person TEXT NOT NULL,
            action_taken TEXT,
            parts_replaced TEXT,
            start_time TEXT,
            end_time TEXT,
            cost REAL DEFAULT 0,
            remark TEXT,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (device_id) REFERENCES devices (id),
            FOREIGN KEY (fault_report_id) REFERENCES fault_reports (id)
        )
    ''')
    
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

def generate_order_no(prefix='WO'):
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT order_no FROM fault_reports 
        WHERE order_no LIKE ? 
        ORDER BY order_no DESC LIMIT 1
    ''', (f'{prefix}{date_str}%',))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        last_no = result['order_no']
        sequence = int(last_no[-4:]) + 1
    else:
        sequence = 1
    
    return f'{prefix}{date_str}{sequence:04d}'

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
        print('Database initialized successfully!')
    else:
        print('Database already exists!')
