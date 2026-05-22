import traceback
from app import app, init_db

try:
    init_db()
    print("数据库初始化成功")
    
    client = app.test_client()
    response = client.get('/api/fault-types')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.get_data(as_text=True)}")
except Exception as e:
    print(f"错误: {e}")
    traceback.print_exc()
