@echo off
echo ========================================
echo 港口集装箱识别终端运维管理系统
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo.
echo [2/3] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告: 依赖安装可能有问题，尝试继续运行...
)

echo.
echo [3/3] 启动服务...
echo.
echo 服务启动后，请访问: http://localhost:5000
echo 按 Ctrl+C 停止服务
echo.
python app.py

pause
