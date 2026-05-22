@echo off
echo ========================================
echo    宠物寄养平台 - 启动脚本
echo ========================================
echo.

echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo Python 环境检查通过
echo.

echo [2/5] 安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 警告: 依赖安装可能有问题，请手动检查
)
echo.

echo [3/5] 创建数据库...
python init_db.py
if %errorlevel% neq 0 (
    echo 错误: 数据库创建失败，请检查 MySQL 是否启动
    pause
    exit /b 1
)
echo.

echo [4/5] 执行数据库迁移...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo 警告: 数据库迁移可能有问题
)
echo.

echo [5/5] 初始化房间数据...
python init_data.py
echo.

echo ========================================
echo    初始化完成！
echo ========================================
echo.
echo 启动开发服务器...
echo 访问地址:
echo   - API 接口: http://127.0.0.1:8000/api/
echo   - 管理后台: http://127.0.0.1:8000/admin/
echo.
echo 提示: 如需创建管理员账号，请在另一个终端执行:
echo       python manage.py createsuperuser
echo.
pause
python manage.py runserver
