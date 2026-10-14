#!/usr/bin/env python3
"""
Palimpsest API Server 启动脚本
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

def check_requirements():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import aiofiles
        print("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_data_directory():
    """检查数据目录"""
    data_dir = Path("data")
    if not data_dir.exists():
        print(f"✗ 数据目录不存在: {data_dir.absolute()}")
        return False
    print(f"✓ 数据目录: {data_dir.absolute()}")
    return True

def main():
    print("=== Palimpsest API Server 启动检查 ===")
    
    # 检查依赖
    if not check_requirements():
        sys.exit(1)
    
    # 检查数据目录
    if not check_data_directory():
        sys.exit(1)
    
    print("\n=== 启动服务器 ===")
    print("访问地址:")
    print("- API文档: http://localhost:8000/docs")
    print("- API根路径: http://localhost:8000/")
    print("- 文件搜索: http://localhost:8000/search?q=关键词")
    print("- 元数据: http://localhost:8000/metadata")
    print("- 目录树: http://localhost:8000/tree")
    print("\n按 Ctrl+C 停止服务器")
    
    # 启动服务器
    try:
        from api_server import app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()