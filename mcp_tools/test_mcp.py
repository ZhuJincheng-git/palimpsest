#!/usr/bin/env python3
"""
Palimpsest MCP Server 简化测试脚本
"""

import asyncio
import json
from pathlib import Path

async def test_server():
    """测试服务器功能"""
    print("🧪 开始测试 Palimpsest MCP Server...")
    
# 创建服务器实例
    data_dir = Path("data")
    from mcp_server import PalimpsestMCPServer
    server = PalimpsestMCPServer(data_dir)
    await server.initialize()
    
    # 测试1: 获取文件树
    print("\n📁 测试1: 获取文件树")
    try:
        tree = await server.get_file_tree("", max_depth=2)
        print(f"✓ 文件树获取成功，包含 {len(tree.get('children', []))} 个子项")
        print(f"📂 根目录: {tree['name']}")
    except Exception as e:
        print(f"✗ 文件树获取失败: {e}")
    
    # 测试2: 列出文件
    print("\n📋 测试2: 列出文件")
    try:
        files = await server.list_files("", recursive=False)
        print(f"✓ 文件列表获取成功，共 {len(files)} 个文件")
        for file in files[:5]:  # 只显示前5个
            print(f"  - {file['path']} ({file['size']} bytes)")
    except Exception as e:
        print(f"✗ 文件列表获取失败: {e}")
    
    # 测试4: 获取文件信息
    print("\n📄 测试4: 获取文件信息")
    try:
        info = await server.get_file_info("README.md")
        print(f"✓ 文件信息获取成功: {info['name']}")
        print(f"  大小: {info['size']} bytes")
        print(f"  类型: {'目录' if info['is_directory'] else '文件'}")
    except Exception as e:
        print(f"✗ 文件信息获取失败: {e}")
    
    # 测试5: 读取文件内容
    print("\n📖 测试5: 读取文件内容")
    try:
        content = await server.get_file_content("README.md")
        print(f"✓ 文件内容读取成功，长度: {len(content)} 字符")
        if len(content) > 100:
            print(f"  预览: {content[:100]}...")
        else:
            print(f"  内容: {content}")
    except Exception as e:
        print(f"✗ 文件内容读取失败: {e}")
    
    # 测试6: 获取元数据
    print("\n📊 测试6: 获取元数据")
    try:
        metadata = await server.get_metadata()
        if metadata:
            print(f"✓ 元数据获取成功")
            print(f"  总文件数: {metadata.get('total_files', 'N/A')}")
            print(f"  总大小: {metadata.get('total_size', 'N/A')} bytes")
        else:
            print("✗ 元数据获取失败")
    except Exception as e:
        print(f"✗ 元数据获取失败: {e}")
    
    print("\n✅ 所有测试完成!")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_server())