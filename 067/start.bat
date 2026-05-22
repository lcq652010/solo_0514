@echo off
echo ========================================
echo 展会管理后端系统 - 快速启动脚本
echo ========================================
echo.

echo [1/5] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/5] 安装依赖包...
pip install -r requirements.txt

echo.
echo [3/5] 执行数据库迁移...
python manage.py makemigrations
python manage.py migrate

echo.
echo [4/5] 初始化演示数据...
python manage.py init_exhibition_data

echo.
echo ========================================
echo 初始化完成！
echo ========================================
echo.
echo 请手动执行以下步骤：
echo 1. 创建超级管理员: python manage.py createsuperuser
echo 2. 启动服务: python manage.py runserver
echo.
echo 访问地址：
echo - API接口: http://127.0.0.1:8000/api/
echo - 管理后台: http://127.0.0.1:8000/admin/
echo.
pause
