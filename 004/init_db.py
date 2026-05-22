"""
数据库初始化脚本 - 创建数据库和表结构
"""
import os
import sys
import pymysql


def create_database():
    """创建数据库"""
    try:
        conn = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '123456'),
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        db_name = os.getenv('DB_NAME', 'campus_supermarket')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"数据库 {db_name} 创建成功或已存在")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"创建数据库失败: {e}")
        return False


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    if create_database():
        print("数据库初始化完成！")
    else:
        print("数据库初始化失败！")
        sys.exit(1)
