#!/usr/bin/env python3
"""
Palimpsest MCP Server 启动脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """检查依赖是否安装"""
    try:
        import mcp
        print("✓ MCP 依赖已安装")
    except ImportError:
        print("✗ MCP 依赖未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "mcp"])
        print("✓ 依赖安装完成")

def check_data_directory():
    """检查数据目录"""
    data_dir = Path("data")
    if not data_dir.exists():
        print(f"✗ 数据目录不存在: {data_dir}")
        sys.exit(1)
    print(f"✓ 数据目录: {data_dir.absolute()}")

def start_server():
    """启动服务器"""
    print("🚀 启动 Palimpsest MCP Server...")
    print("📁 数据目录: data/")
    print("🔧 服务器配置: MCP 标准协议")
    print("🌐 支持功能: 文件树查询、文件读取、文件搜索")
    print("")
    print("使用方法:")
    print("1. 在支持MCP的AI客户端中配置此服务器")
    print("2. 或使用命令行测试: python simple_test.py")
    print("")
    
    # 启动MCP服务器
    subprocess.run([sys.executable, "simple_mcp.py"])

if __name__ == "__main__":
    check_requirements()
    check_data_directory()
    start_server()