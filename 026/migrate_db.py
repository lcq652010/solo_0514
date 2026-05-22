import sqlite3
import os

def migrate_database():
    db_path = 'instance/orders.db'
    
    if not os.path.exists(db_path):
        print('数据库不存在，将在启动时自动创建新表')
        return True
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info('order')")
        columns = [col[1] for col in cursor.fetchall()]
        
        new_columns = [
            ('silk_thread_type', 'VARCHAR(200)'),
            ('pattern_design', 'VARCHAR(200)'),
            ('frame_material', 'VARCHAR(100)'),
            ('fan_size_width', 'VARCHAR(20)'),
            ('fan_size_height', 'VARCHAR(20)'),
            ('kesi_technique', 'VARCHAR(200)'),
            ('kesi_thread_count', 'VARCHAR(50)'),
            ('kesi_color_count', 'INTEGER'),
            ('kesi_completed_at', 'DATETIME'),
            ('kesi_operator', 'VARCHAR(50)'),
            ('frame_type', 'VARCHAR(100)'),
            ('frame_size', 'VARCHAR(50)'),
            ('frame_material_detail', 'VARCHAR(200)'),
            ('frame_completed_at', 'DATETIME'),
            ('frame_operator', 'VARCHAR(50)'),
            ('handle_material', 'VARCHAR(100)'),
            ('handle_style', 'VARCHAR(100)'),
            ('handle_length', 'VARCHAR(20)'),
            ('handle_completed_at', 'DATETIME'),
            ('handle_operator', 'VARCHAR(50)')
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in columns:
                print(f'添加列: {col_name}')
                cursor.execute(f'ALTER TABLE "order" ADD COLUMN {col_name} {col_type}')
        
        conn.commit()
        print('数据库迁移成功！')
        return True
        
    except Exception as e:
        print(f'迁移失败: {e}')
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
