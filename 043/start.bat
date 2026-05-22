@echo off
chcp 65001 >nul
echo ========================================
echo    图书馆管理系统 - 启动脚本
echo ========================================
echo.

echo [1/5] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo Python 环境检查通过
echo.

echo [2/5] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告: 依赖安装可能有问题，请检查网络连接
)
echo 依赖安装完成
echo.

echo [3/5] 生成数据库迁移文件...
python manage.py makemigrations library
if errorlevel 1 (
    echo 错误: 生成迁移文件失败
    pause
    exit /b 1
)
echo 迁移文件生成完成
echo.

echo [4/5] 执行数据库迁移...
python manage.py migrate
if errorlevel 1 (
    echo 错误: 数据库迁移失败，请检查数据库连接配置
    pause
    exit /b 1
)
echo 数据库迁移完成
echo.

echo [5/5] 启动开发服务器...
echo.
echo ========================================
echo  服务启动成功！
echo  API 地址: http://localhost:8000/api/
echo  Admin 后台: http://localhost:8000/admin/
echo  按 Ctrl+C 停止服务
echo ========================================
echo.
python manage.py runserver 0.0.0.0:8000

pause
