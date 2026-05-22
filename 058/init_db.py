import pymysql
import sys


def create_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS pet_fostering CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("数据库 pet_fostering 创建成功或已存在!")
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"创建数据库失败: {e}")
        return False


if __name__ == '__main__':
    success = create_database()
    sys.exit(0 if success else 1)
