import sqlite3

DATABASE = 'ceramic_orders.db'

def migrate_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('PRAGMA table_info(orders)')
        columns = [col[1] for col in cursor.fetchall()]
        
        new_columns = {
            'clay_type': 'TEXT',
            'vessel_size': 'TEXT',
            'glaze_type': 'TEXT',
            'decoration_style': 'TEXT'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in columns:
                print(f'添加字段: {col_name}')
                cursor.execute(f'ALTER TABLE orders ADD COLUMN {col_name} {col_type}')
        
        conn.commit()
        print('数据库迁移完成！')
        
        cursor.execute('PRAGMA table_info(orders)')
        print('\n当前表结构：')
        for col in cursor.fetchall():
            print(f'  {col[1]}: {col[2]}')
            
    except Exception as e:
        print(f'迁移出错: {e}')
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_db()
