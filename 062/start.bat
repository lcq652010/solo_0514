@echo off
echo 正在安装依赖...
pip install -r requirements.txt
echo.
echo 正在启动服务器...
python app.py
pause
