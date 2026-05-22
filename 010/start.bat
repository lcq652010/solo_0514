@echo off
echo ========================================
echo    驾校管理系统后端 - 启动脚本
echo ========================================
echo.

echo [1/5] 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo.
echo [2/5] 安装依赖包...
pip install -r requirements.txt

echo.
echo [3/5] 生成数据库迁移文件...
python manage.py makemigrations

echo.
echo [4/5] 执行数据库迁移...
python manage.py migrate

echo.
echo [5/5] 创建超级管理员账户...
python manage.py createsuperuser

echo.
echo ========================================
echo    初始化完成！
echo ========================================
echo.
echo 启动开发服务器，请运行:
echo   python manage.py runserver
echo.
echo 访问管理后台: http://127.0.0.1:8000/admin/
echo API接口地址: http://127.0.0.1:8000/api/
echo.
pause
