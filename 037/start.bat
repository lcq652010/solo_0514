@echo off
echo ========================================
echo    奶茶店点单系统后端启动脚本
echo ========================================
echo.

echo [1/5] 检查 Python 环境...
python --version
if %errorlevel% neq 0 (
    echo 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/5] 安装依赖包...
pip install -r requirements.txt

echo.
echo [3/5] 数据库迁移...
python manage.py makemigrations
python manage.py migrate

echo.
echo [4/5] 初始化示例数据...
python init_data.py

echo.
echo [5/5] 启动服务...
echo.
echo 服务启动后访问：
echo   API 地址: http://localhost:8000/api/
echo   后台管理: http://localhost:8000/admin/
echo.
echo 按 Ctrl+C 停止服务
echo.
python manage.py runserver 0.0.0.0:8000

pause
