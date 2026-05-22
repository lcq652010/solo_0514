import sqlite3

DATABASE = 'ceramic_orders.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_address TEXT,
            brush_washer_type TEXT NOT NULL,
            size TEXT NOT NULL,
            color TEXT NOT NULL,
            design_requirements TEXT,
            quantity INTEGER NOT NULL DEFAULT 1,
            estimated_price REAL,
            status TEXT NOT NULL DEFAULT '待接单',
            remark TEXT,
            clay_type TEXT,
            vessel_size TEXT,
            glaze_type TEXT,
            decoration_style TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("数据库初始化成功！")

if __name__ == '__main__':
    init_db()
