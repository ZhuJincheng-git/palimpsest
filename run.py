#!/usr/bin/env python3
"""
简单的启动脚本 - 无需额外依赖检查
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("=== 启动 Palimpsest API Server ===")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 检查data目录
    data_dir = Path("data")
    if not data_dir.exists():
        print(f"错误: data目录不存在: {data_dir.absolute()}")
        sys.exit(1)
    
    print(f"数据目录: {data_dir.absolute()}")
    print("启动服务器...")
    print("访问地址:")
    print("  API文档: http://localhost:8000/docs")
    print("  API根路径: http://localhost:8000/")
    print("  搜索: http://localhost:8000/search?q=关键词")
    print("\n按 Ctrl+C 停止服务器")
    
    # 启动服务器
    try:
        subprocess.run([sys.executable, "api_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except subprocess.CalledProcessError as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()