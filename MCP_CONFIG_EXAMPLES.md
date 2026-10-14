# MCP Server 配置示例

## Claude Desktop 配置

文件路径: `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "palimpsest": {
      "command": "python",
      "args": ["/path/to/palimpsest/simple_mcp.py"],
      "env": {
        "PYTHONPATH": "/path/to/palimpsest"
      }
    }
  }
}
```

## OpenAI ChatGPT 配置

对于支持MCP的ChatGPT插件，可以使用以下配置：

```json
{
  "name": "Palimpsest File System",
  "server": {
    "command": "python",
    "args": ["/path/to/palimpsest/simple_mcp.py"],
    "env": {
      "PYTHONPATH": "/path/to/palimpsest"
    }
  },
  "tools": [
    {
      "name": "read_file",
      "description": "读取文件内容"
    },
    {
      "name": "list_files",
      "description": "列出指定目录下的文件"
    },
    {
      "name": "get_file_tree",
      "description": "获取指定目录的文件树结构"
    },
    {
      "name": "search_files",
      "description": "在文件系统中搜索文件"
    },
    {
      "name": "get_file_info",
      "description": "获取文件的基本信息"
    },
    {
      "name": "get_metadata",
      "description": "获取系统元数据"
    }
  ]
}
```

## VSCode MCP 配置

对于VSCode的MCP扩展，配置如下：

```json
{
  "mcp.servers": {
    "palimpsest": {
      "command": "python",
      "args": ["/path/to/palimpsest/simple_mcp.py"],
      "env": {
        "PYTHONPATH": "/path/to/palimpsest"
      }
    }
  }
}
```

## 命令行测试

你可以使用curl来测试MCP服务器：

```bash
# 初始化服务器
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | python simple_mcp.py

# 获取工具列表
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}' | python simple_mcp.py

# 读取文件
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "read_file", "arguments": {"file_path": "README.md"}}}' | python simple_mcp.py

# 获取文件树
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_file_tree", "arguments": {"path": "", "max_depth": 2}}}' | python simple_mcp.py

# 搜索文件
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "search_files", "arguments": {"query": "README", "limit": 10}}}' | python simple_mcp.py
```

## Python 客户端示例

```python
import asyncio
import json
import sys
from pathlib import Path

class MCPClient:
    def __init__(self, server_path):
        self.server_path = server_path
        
    async def call_tool(self, method, arguments=None):
        """调用工具"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": arguments or {}
        }
        
        process = await asyncio.create_subprocess_exec(
            sys.executable, self.server_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate(
            input=json.dumps(request).encode()
        )
        
        if process.returncode != 0:
            raise Exception(f"Server error: {stderr.decode()}")
        
        response = json.loads(stdout.decode())
        if "error" in response:
            raise Exception(f"RPC error: {response['error']['message']}")
        
        return response.get("result", {})

async def main():
    client = MCPClient("simple_mcp.py")
    
    # 初始化
    await client.call_tool("initialize")
    
    # 获取工具列表
    tools = await client.call_tool("tools/list")
    print("可用工具:", len(tools["tools"]))
    
    # 读取文件
    result = await client.call_tool("tools/call", {
        "name": "read_file",
        "arguments": {"file_path": "README.md"}
    })
    print("文件内容:", result["content"][0]["text"][:100] + "...")
    
    # 获取文件树
    result = await client.call_tool("tools/call", {
        "name": "get_file_tree",
        "arguments": {"path": "", "max_depth": 1}
    })
    print("文件树:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
```

## 环境变量配置

你可以通过环境变量来配置服务器：

```bash
# 设置数据目录
export PALIMPSEST_DATA_DIR="/path/to/data"

# 设置日志级别
export PALIMPSEST_LOG_LEVEL="INFO"

# 设置最大文件大小限制（字节）
export PALIMPSEST_MAX_FILE_SIZE="10485760"  # 10MB
```

## Docker 配置

如果你想在Docker中运行这个服务器：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "simple_mcp.py"]
```

然后运行：
```bash
docker build -t palimpsest-mcp .
docker run -v $(pwd)/data:/app/data palimpsest-mcp
```