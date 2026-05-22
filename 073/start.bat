@echo off
echo ====================================
echo    驾校管理系统后端启动脚本
echo ====================================
echo.

echo [1/4] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/4] 安装依赖包...
pip install -r requirements.txt

echo.
echo [3/4] 执行数据库迁移...
python manage.py makemigrations
python manage.py migrate

echo.
echo [4/4] 启动开发服务器...
echo.
echo 服务启动后，请访问:
echo   API 文档: http://localhost:8000/api/
echo   管理后台: http://localhost:8000/admin/
echo.
echo 按 Ctrl+C 停止服务
echo.

python manage.py runserver
