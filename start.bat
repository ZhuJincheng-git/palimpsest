@echo off
echo === 启动 Palimpsest API Server ===
echo.
echo 正在检查依赖...
python -c "import fastapi, uvicorn, aiofiles" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
)
echo.
echo 数据目录检查...
if not exist "data" (
    echo 错误: data目录不存在
    pause
    exit /b 1
)
echo.
echo 启动服务器...
echo 访问地址:
echo   API文档: http://localhost:8000/docs
echo   API根路径: http://localhost:8000/
echo.
python api_server.py
pause