#!/usr/bin/env python3
"""
Palimpsest MCP Server 测试脚本
"""

import asyncio
import json
import sys
from pathlib import Path

# 导入我们的服务器实现
sys.path.append('.')
from mcp_server import PalimpsestMCPServer

async def test_server():
    """测试服务器功能"""
    print("🧪 开始测试 Palimpsest MCP Server...")
    
    # 创建服务器实例
    data_dir = Path("data")
    server = PalimpsestMCPServer(data_dir)
    await server.initialize()
    
    # 测试1: 获取文件树
    print("\n📁 测试1: 获取文件树")
    try:
        tree = await server.get_file_tree("data", max_depth=2)
        print(f"✓ 文件树获取成功，包含 {len(tree.get('children', []))} 个子项")
        print(f"📂 根目录: {tree['name']}")
    except Exception as e:
        print(f"✗ 文件树获取失败: {e}")
    
    # 测试2: 列出文件
    print("\n📋 测试2: 列出文件")
    try:
        files = await server.list_files("data", recursive=False)
        print(f"✓ 文件列表获取成功，共 {len(files)} 个文件")
        for file in files[:5]:  # 只显示前5个
            print(f"  - {file['path']} ({file['size']} bytes)")
    except Exception as e:
        print(f"✗ 文件列表获取失败: {e}")
    
    # 测试3: 搜索文件
    print("\n🔍 测试3: 搜索文件")
    try:
        results = await server.search_files("README", limit=10)
        print(f"✓ 搜索完成，找到 {len(results)} 个匹配文件")
        for result in results[:3]:  # 只显示前3个
            print(f"  - {result['path']}")
    except Exception as e:
        print(f"✗ 搜索失败: {e}")
    
    # 测试4: 获取文件信息
    print("\n📄 测试4: 获取文件信息")
    try:
        info = await server.get_file_info("data/README.md")
        print(f"✓ 文件信息获取成功: {info['name']}")
        print(f"  大小: {info['size']} bytes")
        print(f"  类型: {'目录' if info['is_directory'] else '文件'}")
    except Exception as e:
        print(f"✗ 文件信息获取失败: {e}")
    
    # 测试5: 读取文件内容
    print("\n📖 测试5: 读取文件内容")
    try:
        content = await server.get_file_content("data/README.md")
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

async def test_tool_calls():
    """测试工具调用"""
    print("\n🔧 测试工具调用...")
    
    # 模拟工具调用
    server = Server("test-server")
    
    @server.list_tools()
    async def list_tools():
        return [
            types.Tool(
                name="list_files",
                description="列出文件",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "default": ""}
                    }
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "list_files":
            data_dir = Path("data")
            palimpsest = PalimpsestMCPServer(data_dir)
            await palimpsest.initialize()
            files = await palimpsest.list_files(arguments.get("path", ""))
            return [types.TextContent(type="text", text=json.dumps(files, indent=2))]
    
    # 这里可以添加更多的工具调用测试
    print("✅ 工具调用测试框架已设置")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_server())
    asyncio.run(test_tool_calls())