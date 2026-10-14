#!/bin/bash
echo "=== 启动 Palimpsest API Server ==="
echo ""
echo "正在检查依赖..."
python3 -c "import fastapi, uvicorn, aiofiles" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
fi
echo ""
echo "数据目录检查..."
if [ ! -d "data" ]; then
    echo "错误: data目录不存在"
    exit 1
fi
echo ""
echo "启动服务器..."
echo "访问地址:"
echo "  API文档: http://localhost:8000/docs"
echo "  API根路径: http://localhost:8000/"
echo ""
python3 api_server.py