# Palimpsest MCP Server

高性能、简洁、高质量的MCP (Model Context Protocol) 服务器，支持通过AI模型访问data/内的文件，支持文件树查询和全文搜索。

## 特性

- 🚀 **高性能**: 使用异步I/O，支持高并发
- 📁 **文件树查询**: 支持多层递归的文件树结构查询
- 🔍 **强大搜索**: 支持全文搜索，模糊匹配
- 📊 **元数据支持**: 自动读取和缓存文件元数据
- 🌐 **MCP标准**: 符合Model Context Protocol规范
- 🔧 **简洁设计**: 代码简洁，易于维护
- 🛡️ **安全访问**: 文件访问限制在data/目录内

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python start.py
```

### 3. 测试服务器

```bash
python test_mcp.py
```

### 4. 配置AI客户端

参考 `MCP_CONFIG_EXAMPLES.md` 文件，配置支持MCP的AI客户端。

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

## 使用示例

### Python 客户端示例

```python
import asyncio
import json
from mcp_server import PalimpsestMCPServer

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

### 命令行测试

```bash
# 测试文件树查询
python -c "
import asyncio
from mcp_server import PalimpsestMCPServer
async def test():
    s = PalimpsestMCPServer(Path('data'))
    await s.initialize()
    tree = await s.get_file_tree('', max_depth=2)
    print('文件树:', json.dumps(tree, indent=2, ensure_ascii=False))
asyncio.run(test())
"

# 测试文件搜索
python -c "
import asyncio
from mcp_server import PalimpsestMCPServer
async def test():
    s = PalimpsestMCPServer(Path('data'))
    await s.initialize()
    results = await s.search_files('README', limit=5)
    print('搜索结果:', json.dumps(results, indent=2, ensure_ascii=False))
asyncio.run(test())
"
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
python mcp_server.py
```

## 文档

- [MCP配置示例](MCP_CONFIG_EXAMPLES.md) - 详细的客户端配置示例
- [完整文档](MCP_COMPLETE_README.md) - 完整的技术文档和API说明

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