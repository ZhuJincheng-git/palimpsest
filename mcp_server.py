#!/usr/bin/env python3
"""
Palimpsest MCP Server
符合Model Context Protocol (MCP)标准的服务器，支持文件系统操作
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
import mcp
import mcp.server.stdio
import mcp.types as types
import hashlib
from datetime import datetime

# 全局变量
DATA_DIR = Path("data")
METADATA_FILE = DATA_DIR / "metadata.json"

class PalimpsestMCPServer:
    """Palimpsest MCP服务器"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._metadata_cache = None
        self._metadata_hash = None
        
    async def initialize(self):
        """初始化服务器"""
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")
        
        logging.info(f"Initialized Palimpsest MCP server with data directory: {self.data_dir.absolute()}")
    
    async def get_file_tree(self, path: str = "", max_depth: int = 10) -> Dict[str, Any]:
        """
        获取文件树结构
        
        Args:
            path: 相对路径，默认为根目录
            max_depth: 最大递归深度，防止无限递归
            
        Returns:
            文件树结构
        """
        full_path = self.data_dir / path
        
        if not full_path.exists():
            raise ValueError(f"Path not found: {path}")
        
        async def _build_tree(current_path: Path, current_depth: int) -> Dict[str, Any]:
            if current_depth >= max_depth:
                return {"path": str(current_path.relative_to(self.data_dir)), "type": "directory"}
            
            tree = {
                "path": str(current_path.relative_to(self.data_dir)),
                "name": current_path.name,
                "type": "directory" if current_path.is_dir() else "file",
                "children": []
            }
            
            if current_path.is_dir():
                try:
                    for item in sorted(current_path.iterdir()):
                        if item.name.startswith('.'):
                            continue  # 跳过隐藏文件
                        tree["children"].append(await _build_tree(item, current_depth + 1))
                except PermissionError:
                    logging.warning(f"Permission denied: {current_path}")
            
            return tree
        
        return await _build_tree(full_path, 0)
    
    async def list_files(self, path: str = "", recursive: bool = True) -> List[Dict[str, Any]]:
        """
        列出指定目录下的文件
        
        Args:
            path: 相对路径，默认为根目录
            recursive: 是否递归列出子目录
            
        Returns:
            文件信息列表
        """
        full_path = self.data_dir / path
        
        if not full_path.exists():
            raise ValueError(f"Path not found: {path}")
        
        files = []
        
        def _scan_directory(current_path: Path):
            nonlocal files
            
            try:
                if current_path.is_file():
                    stat = current_path.stat()
                    files.append({
                        "path": str(current_path.relative_to(self.data_dir)),
                        "name": current_path.name,
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "created": stat.st_ctime,
                        "extension": current_path.suffix.lower(),
                        "type": "file"
                    })
                elif current_path.is_dir() and recursive:
                    for item in sorted(current_path.iterdir()):
                        if item.name.startswith('.'):
                            continue  # 跳过隐藏文件
                        _scan_directory(item)
            except (PermissionError, OSError) as e:
                logging.warning(f"Error scanning {current_path}: {e}")
        
        _scan_directory(full_path)
        return files
    
    async def get_file_content(self, file_path: str) -> str:
        """
        获取文件内容
        
        Args:
            file_path: 文件相对路径
            
        Returns:
            文件内容
        """
        full_path = self.data_dir / file_path
        
        if not full_path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        if not full_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # 二进制文件返回base64编码
            with open(full_path, 'rb') as f:
                content = f.read()
                return content.hex()
        except Exception as e:
            raise ValueError(f"Failed to read file: {str(e)}")
    
    async def search_files(self, query: str, path: str = "", limit: int = 100) -> List[Dict[str, Any]]:
        """
        搜索文件
        
        Args:
            query: 搜索关键词
            path: 搜索路径，默认为根目录
            limit: 返回结果数量限制
            
        Returns:
            匹配的文件列表
        """
        results = []
        query_lower = query.lower()
        full_path = self.data_dir / path
        
        if not full_path.exists():
            raise ValueError(f"Path not found: {path}")
        
        def _search(current_path: Path):
            nonlocal results
            
            try:
                if current_path.is_file():
                    relative_path = str(current_path.relative_to(self.data_dir))
                    if query_lower in relative_path.lower():
                        stat = current_path.stat()
                        results.append({
                            "path": relative_path,
                            "name": current_path.name,
                            "size": stat.st_size,
                            "modified": stat.st_mtime
                        })
                        
                        if len(results) >= limit:
                            return
                
                elif current_path.is_dir():
                    for item in current_path.iterdir():
                        if item.name.startswith('.'):
                            continue  # 跳过隐藏文件
                        _search(item)
                        
                        if len(results) >= limit:
                            return
            except (PermissionError, OSError) as e:
                logging.warning(f"Error searching {current_path}: {e}")
        
        _search(full_path)
        return results
    
    async def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            file_path: 文件相对路径
            
        Returns:
            文件信息
        """
        full_path = self.data_dir / file_path
        
        if not full_path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        stat = full_path.stat()
        return {
            "path": file_path,
            "name": full_path.name,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "extension": full_path.suffix.lower(),
            "is_directory": full_path.is_dir(),
            "is_file": full_path.is_file()
        }
    
    async def get_metadata(self) -> Optional[Dict[str, Any]]:
        """获取元数据"""
        try:
            if self._metadata_cache and self._metadata_hash:
                # 检查文件是否被修改
                current_hash = self._calculate_file_hash(METADATA_FILE)
                if current_hash == self._metadata_hash:
                    return self._metadata_cache
            
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                self._metadata_cache = json.loads(content)
                self._metadata_hash = self._calculate_file_hash(METADATA_FILE)
                return self._metadata_cache
        except Exception:
            return None
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

# 创建服务器实例
server = mcp.server.Server("palimpsest-mcp")
palimpsest_server = PalimpsestMCPServer(DATA_DIR)

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """列出可用工具"""
    return [
        types.Tool(
            name="read_file",
            description="读取文件内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件相对路径，例如 'raw/autobiography/README.md'"
                    }
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="list_files",
            description="列出指定目录下的文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "目录相对路径，例如 'raw/'，默认为根目录 ''",
                        "default": ""
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "是否递归列出子目录",
                        "default": True
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="get_file_tree",
            description="获取指定目录的文件树结构",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "目录相对路径，例如 'raw/'，默认为根目录 ''",
                        "default": ""
                    },
                    "max_depth": {
                        "type": "integer",
                        "description": "最大递归深度，防止无限递归",
                        "default": 10
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="search_files",
            description="在文件系统中搜索文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "path": {
                        "type": "string",
                        "description": "搜索路径，例如 'raw/'，默认为根目录 ''",
                        "default": ""
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回结果数量限制",
                        "default": 100
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_file_info",
            description="获取文件的基本信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件相对路径，例如 'raw/autobiography/README.md'"
                    }
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="get_metadata",
            description="获取系统元数据",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """调用工具"""
    try:
        if name == "read_file":
            file_path = arguments.get("file_path", "")
            content = await palimpsest_server.get_file_content(file_path)
            return [types.TextContent(type="text", text=content)]
        
        elif name == "list_files":
            path = arguments.get("path", "")
            recursive = arguments.get("recursive", True)
            files = await palimpsest_server.list_files(path, recursive)
            return [types.TextContent(type="text", text=json.dumps(files, indent=2, ensure_ascii=False))]
        
        elif name == "get_file_tree":
            path = arguments.get("path", "")
            max_depth = arguments.get("max_depth", 10)
            tree = await palimpsest_server.get_file_tree(path, max_depth)
            return [types.TextContent(type="text", text=json.dumps(tree, indent=2, ensure_ascii=False))]
        
        elif name == "search_files":
            query = arguments.get("query", "")
            path = arguments.get("path", "")
            limit = arguments.get("limit", 100)
            results = await palimpsest_server.search_files(query, path, limit)
            return [types.TextContent(type="text", text=json.dumps(results, indent=2, ensure_ascii=False))]
        
        elif name == "get_file_info":
            file_path = arguments.get("file_path", "")
            info = await palimpsest_server.get_file_info(file_path)
            return [types.TextContent(type="text", text=json.dumps(info, indent=2, ensure_ascii=False))]
        
        elif name == "get_metadata":
            metadata = await palimpsest_server.get_metadata()
            return [types.TextContent(type="text", text=json.dumps(metadata, indent=2, ensure_ascii=False))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logging.error(f"Error calling tool {name}: {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """主函数"""
    await palimpsest_server.initialize()
    
    # 使用stdio作为传输层
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            {}
        )

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    asyncio.run(main())