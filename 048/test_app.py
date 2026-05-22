import sys
sys.path.insert(0, '.')

from app import app

print('Flask应用路由列表:')
for rule in app.url_map.iter_rules():
    if not rule.endpoint.startswith('static'):
        print(f'  {rule.endpoint}: {rule.rule}')

print('\n测试数据库初始化...')
with app.app_context():
    from app import get_db
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print('数据库表:', [t['name'] for t in tables])
    except Exception as e:
        print('数据库错误:', e)

print('\n测试完成!')
