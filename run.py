#!/usr/bin/env python3
"""
Palimpsest 项目运行脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("=== Palimpsest 项目 ===")
    print("1. 启动 MCP Server")
    print("2. 运行测试")
    print("3. 查看文档")
    print("4. 退出")
    
    while True:
        choice = input("\n请选择操作 (1-4): ").strip()
        
        if choice == "1":
            print("\n=== 启动 MCP Server ===")
            # 检Python版本
            if sys.version_info < (3, 8):
                print("错误: 需要Python 3.8或更高版本")
                continue
            
            # 检data目录
            data_dir = Path("data")
            if not data_dir.exists():
                print(f"错误: data目录不存在: {data_dir.absolute()}")
                continue
            
            print(f"数据目录: {data_dir.absolute()}")
            print("启动 MCP Server...")
            print("使用 Ctrl+C 停止服务器")
            
            # 启动服务器
            try:
                subprocess.run([sys.executable, "start.py"])
            except KeyboardInterrupt:
                print("\n服务器已停止")
            except subprocess.CalledProcessError as e:
                print(f"启动失败: {e}")
        
        elif choice == "2":
            print("\n=== 运行测试 ===")
            try:
                subprocess.run([sys.executable, "test_mcp.py"])
            except subprocess.CalledProcessError as e:
                print(f"测试失败: {e}")
        
        elif choice == "3":
            print("\n=== 文档 ===")
            print("1. API文档 (API_README.md)")
            print("2. MCP配置示例 (MCP_CONFIG_EXAMPLES.md)")
            print("3. 项目说明 (README.md)")
            
            doc_choice = input("选择文档 (1-3): ").strip()
            if doc_choice == "1":
                os.system("cat API_README.md")
            elif doc_choice == "2":
                os.system("cat MCP_CONFIG_EXAMPLES.md")
            elif doc_choice == "3":
                os.system("cat README.md")
        
        elif choice == "4":
            print("退出")
            break
        
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()