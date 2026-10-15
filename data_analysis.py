#!/usr/bin/env python3
"""
Palimpsest 数据分析工具启动脚本
简化用户操作，提供便捷的数据管理功能
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """运行shell命令"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("错误:", result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        print(f"错误输出: {e.stderr}", file=sys.stderr)
        return False
    return True

def main():
    print("=== Palimpsest 数据分析工具 ===")
    print()
    
    # 检查data目录是否存在
    data_dir = Path("data")
    if not data_dir.exists():
        print("错误: data/ 目录不存在")
        sys.exit(1)
    
    print(f"数据目录: {data_dir.absolute()}")
    print()
    
    while True:
        print("请选择操作:")
        print("1. 初始化数据监控")
        print("2. 检查数据变化")
        print("3. 更新数据监控")
        print("4. 查看更新历史")
        print("5. 详细模式检查变化")
        print("6. 详细模式查看历史")
        print("0. 退出")
        print()
        
        try:
            choice = input("请输入选项 (0-6): ").strip()
        except KeyboardInterrupt:
            print("\n退出程序")
            break
        except EOFError:
            print("\n退出程序")
            break
        
        print()
        
        if choice == "0":
            print("感谢使用 Palimpsest 数据分析工具！")
            break
        elif choice == "1":
            print("正在初始化数据监控...")
            success = run_command("python3 data_tools/file_monitor.py data --init")
            if success:
                print("初始化完成！")
        elif choice == "2":
            print("正在检查数据变化...")
            success = run_command("python3 data_tools/file_monitor.py data --check")
            if success:
                print("检查完成！")
        elif choice == "3":
            description = input("请输入更新说明（可选，直接回车跳过）: ").strip()
            if description:
                cmd = f"python3 data_tools/file_monitor.py data --update --description \"{description}\""
            else:
                cmd = "python3 data_tools/file_monitor.py data --update"
            print("正在更新数据监控...")
            success = run_command(cmd)
            if success:
                print("更新完成！")
        elif choice == "4":
            limit = input("请输入显示条数（默认5，直接回车使用默认）: ").strip()
            if limit:
                cmd = f"python3 data_tools/file_monitor.py data --history --limit {limit}"
            else:
                cmd = "python3 data_tools/file_monitor.py data --history --limit 5"
            print("正在查看更新历史...")
            success = run_command(cmd)
            if success:
                print("查看完成！")
        elif choice == "5":
            print("正在详细检查数据变化...")
            success = run_command("python3 data_tools/file_monitor.py data --check --verbose")
            if success:
                print("详细检查完成！")
        elif choice == "6":
            limit = input("请输入显示条数（默认5，直接回车使用默认）: ").strip()
            if limit:
                cmd = f"python3 data_tools/file_monitor.py data --history --limit {limit} --verbose"
            else:
                cmd = "python3 data_tools/file_monitor.py data --history --limit 5 --verbose"
            print("正在详细查看更新历史...")
            success = run_command(cmd)
            if success:
                print("详细查看完成！")
        else:
            print("无效选项，请重新输入！")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()