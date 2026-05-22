@echo off
echo ========================================
echo 汽车租赁管理系统 - 启动脚本
echo ========================================
echo.

echo [1/6] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/6] 安装依赖包...
pip install -r requirements.txt

echo.
echo [3/6] 生成数据库迁移文件...
python manage.py makemigrations

echo.
echo [4/6] 执行数据库迁移...
python manage.py migrate

echo.
echo [5/6] 初始化测试数据...
python manage.py initdata

echo.
echo [6/6] 启动开发服务器...
echo ========================================
echo 服务启动成功！
echo 管理后台: http://localhost:8000/admin/
echo API 地址: http://localhost:8000/api/
echo ========================================
echo.
echo 首次使用请创建超级管理员账号:
echo 执行命令: python manage.py createsuperuser
echo.

python manage.py runserver 0.0.0.0:8000

pause
