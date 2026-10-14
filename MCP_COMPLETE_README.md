# Palimpsest MCP Server 完整配置

## 概述

Palimpsest MCP Server 是一个符合 Model Context Protocol (MCP) 标准的服务器，专门为AI模型提供文件系统访问能力。它支持文件树查询、文件读取、文件搜索等功能，特别适合用于AI对用户个人数据的分析。

## 核心功能

### 📁 文件树查询
- 支持多层递归的文件树结构查询
- 可指定最大递归深度，防止无限递归
- 自动跳过隐藏文件（以`.`开头的文件）

### 📄 文件操作
- **文件读取**: 支持文本和二进制文件读取
- **文件信息**: 获取文件的元数据信息（大小、修改时间、创建时间等）
- **文件列表**: 支持递归或非递归的文件列表获取

### 🔍 搜索功能
- 支持关键词搜索
- 可指定搜索路径和限制结果数量
- 搜索结果包含文件路径、名称、大小和修改时间

### 📊 系统信息
- 获取系统元数据（总文件数、总大小等）
- 元数据缓存机制，提高性能

## MCP工具列表

### 1. read_file
读取文件内容
- **参数**: 
  - `file_path` (string): 文件相对路径，例如 'README.md'
- **返回**: 文件内容

### 2. list_files
列出指定目录下的文件
- **参数**:
  - `path` (string, 可选): 目录相对路径，默认为根目录 ''
  - `recursive` (boolean, 可选): 是否递归列出子目录，默认为True
- **返回**: 文件信息列表

### 3. get_file_tree
获取指定目录的文件树结构
- **参数**:
  - `path` (string, 可选): 目录相对路径，默认为根目录 ''
  - `max_depth` (integer, 可选): 最大递归深度，默认为10
- **返回**: 文件树结构

### 4. search_files
在文件系统中搜索文件
- **参数**:
  - `query` (string): 搜索关键词
  - `path` (string, 可选): 搜索路径，默认为根目录 ''
  - `limit` (integer, 可选): 返回结果数量限制，默认为100
- **返回**: 匹配的文件列表

### 5. get_file_info
获取文件的基本信息
- **参数**:
  - `file_path` (string): 文件相对路径
- **返回**: 文件信息

### 6. get_metadata
获取系统元数据
- **参数**: 无
- **返回**: 系统统计信息

## 安装和配置

### 1. 环境要求
- Python 3.8+
- MCP 依赖包

### 2. 安装依赖
```bash
pip install mcp
```

### 3. 启动服务器
```bash
python simple_mcp.py
```

### 4. 测试服务器
```bash
python simple_test.py
```

## 使用示例

### 在AI客户端中配置

#### Claude Desktop配置
在 `claude_desktop_config.json` 中添加：
```json
{
  "mcpServers": {
    "palimpsest": {
      "command": "python",
      "args": ["/path/to/palimpsest/simple_mcp.py"],
      "env": {}
    }
  }
}
```

#### 其他支持MCP的客户端
参考相应客户端的MCP配置文档

### 命令行测试示例

```python
import asyncio
import json
from simple_mcp import PalimpsestMCPServer

async def example_usage():
    server = PalimpsestMCPServer(Path("data"))
    await server.initialize()
    
    # 获取文件树
    tree = await server.get_file_tree("", max_depth=2)
    print("文件树:", json.dumps(tree, indent=2, ensure_ascii=False))
    
    # 搜索文件
    results = await server.search_files("README", limit=5)
    print("搜索结果:", json.dumps(results, indent=2, ensure_ascii=False))
    
    # 读取文件
    content = await server.get_file_content("README.md")
    print("文件内容预览:", content[:200] + "...")

asyncio.run(example_usage())
```

## 安全特性

### 🔒 访问控制
- **文件访问限制**: 服务器只能访问 `data/` 目录及其子目录
- **路径遍历防护**: 防止 `../` 等路径遍历攻击
- **权限检查**: 自动跳过没有权限访问的目录

### 🛡️ 安全机制
- **隐藏文件过滤**: 自动跳过以 `.` 开头的隐藏文件
- **深度限制**: 文件树查询有最大深度限制，防止无限递归
- **错误处理**: 完善的异常处理机制

## 性能优化

### 📊 缓存机制
- **元数据缓存**: 系统元数据会被缓存，提高重复查询性能
- **哈希校验**: 使用SHA256哈希值检测文件变化

### ⚡ 异步处理
- **异步I/O**: 所有文件操作都是异步的，提高并发性能
- **流式处理**: 大文件采用流式处理，避免内存溢出

## API接口说明

### 请求格式
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "file_path": "README.md"
    }
  }
}
```

### 响应格式
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "文件内容..."
      }
    ]
  }
}
```

## 故障排除

### 常见问题

1. **ImportError: No module named 'mcp'**
   ```bash
   pip install mcp
   ```

2. **FileNotFoundError: Data directory not found**
   - 确保data/目录存在
   - 检查路径是否正确

3. **PermissionError: [Errno 13] Permission denied**
   - 检查data/目录的访问权限
   - 确保运行用户有读取权限

### 调试模式
设置环境变量启用调试日志：
```bash
export MCP_DEBUG=1
python simple_mcp.py
```

## 更新日志

### v1.0.0 (2026-10-14)
- 初始版本发布
- 支持基本的文件操作功能
- 符合MCP标准协议
- 支持文件树查询功能
- 实现了6个核心工具

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目采用MIT许可证。