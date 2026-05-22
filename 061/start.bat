@echo off
echo ========================================
echo    运动场馆管理后端系统 - 快速启动
echo ========================================
echo.

echo [1/5] 检查 Python 环境...
python --version
if %errorlevel% neq 0 (
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
echo [4/5] 初始化测试数据...
python init_data.py

echo.
echo [5/5] 启动开发服务器...
echo.
echo ========================================
echo    服务启动成功！
echo ========================================
echo API 地址: http://127.0.0.1:8000/api/
echo 管理后台: http://127.0.0.1:8000/admin/
echo 管理员账号: admin / admin123
echo 测试用户: testuser / test123
echo ========================================
echo.
echo 按 Ctrl+C 停止服务
echo.

python manage.py runserver

pause
