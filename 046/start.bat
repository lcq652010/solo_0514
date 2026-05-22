@echo off
echo ======================================
echo 家政服务平台后端启动脚本
echo ======================================
echo.

echo [1/5] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/5] 安装依赖包...
pip install -r requirements.txt

echo.
echo [3/5] 创建数据库迁移...
python manage.py makemigrations

echo.
echo [4/5] 执行数据库迁移...
python manage.py migrate

echo.
echo [5/5] 启动开发服务器...
echo.
echo ======================================
echo 服务器启动成功!
echo 访问地址: http://localhost:8000
echo API文档: http://localhost:8000/api/
echo 后台管理: http://localhost:8000/admin/
echo ======================================
echo.
echo 提示: 如需创建超级管理员，请运行: python manage.py createsuperuser
echo       如需初始化测试数据，请运行: python init_data.py
echo.

python manage.py runserver

pause
