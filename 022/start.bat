@echo off
echo ========================================
echo  线上课程平台后端启动脚本
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
if errorlevel 1 (
    echo 警告: 依赖安装可能有问题，继续尝试运行...
)
echo.

echo [3/6] 生成数据库迁移文件...
python manage.py makemigrations
if errorlevel 1 (
    echo 错误: 数据库迁移失败
    pause
    exit /b 1
)
echo.

echo [4/6] 执行数据库迁移...
python manage.py migrate
if errorlevel 1 (
    echo 错误: 数据库迁移执行失败
    pause
    exit /b 1
)
echo.

echo [5/6] 初始化演示数据...
python init_db.py
echo.

echo [6/6] 启动开发服务器...
echo.
echo 服务地址: http://127.0.0.1:8000/
echo API 文档: http://127.0.0.1:8000/api/
echo 后台管理: http://127.0.0.1:8000/admin/
echo.
echo 测试账号:
echo   讲师: teacher / teacher123
echo   学生: student / student123
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
python manage.py runserver

pause
