#!/usr/bin/env python3
"""
Palimpsest API Server
高性能、简洁、高质量的Python服务端，支持通过API读取data/内文件，支持全data文件名搜索
"""

import os
import json
import asyncio
import aiofiles
from pathlib import Path
from typing import List, Dict, Optional, Union
from fastapi import FastAPI, HTTPException, Query, Path as PathParam
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import hashlib
from datetime import datetime

app = FastAPI(
    title="Palimpsest API",
    description="高性能文件API服务，支持读取data/目录下的所有文件",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
DATA_DIR = Path("data")
METADATA_FILE = DATA_DIR / "metadata.json"

class FileManager:
    """高性能文件管理器"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._metadata_cache = None
        self._metadata_hash = None
        
    async def get_file_content(self, file_path: str) -> str:
        """异步获取文件内容"""
        full_path = self.data_dir / file_path
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        try:
            async with aiofiles.open(full_path, 'r', encoding='utf-8') as f:
                return await f.read()
        except UnicodeDecodeError:
            # 二进制文件返回base64编码
            async with aiofiles.open(full_path, 'rb') as f:
                content = await f.read()
                return content.hex()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")
    
    async def get_file_info(self, file_path: str) -> Dict:
        """获取文件信息"""
        full_path = self.data_dir / file_path
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        stat = full_path.stat()
        return {
            "path": file_path,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "extension": full_path.suffix.lower(),
            "is_directory": full_path.is_dir()
        }
    
    async def search_files(self, query: str, limit: int = 100) -> List[Dict]:
        """搜索文件名"""
        results = []
        query_lower = query.lower()
        
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                file_path = Path(root) / file
                relative_path = str(file_path.relative_to(self.data_dir))
                
                if query_lower in relative_path.lower():
                    results.append({
                        "path": relative_path,
                        "name": file,
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime
                    })
                    
                    if len(results) >= limit:
                        break
            
            if len(results) >= limit:
                break
        
        return results
    
    async def get_directory_tree(self, path: str = "") -> Dict:
        """获取目录树结构"""
        full_path = self.data_dir / path
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Directory not found")
        
        tree = {
            "path": path,
            "name": full_path.name,
            "type": "directory",
            "children": []
        }
        
        try:
            for item in sorted(full_path.iterdir()):
                relative_path = str(item.relative_to(self.data_dir))
                if item.is_dir():
                    tree["children"].append({
                        "path": relative_path,
                        "name": item.name,
                        "type": "directory"
                    })
                else:
                    stat = item.stat()
                    tree["children"].append({
                        "path": relative_path,
                        "name": item.name,
                        "type": "file",
                        "size": stat.st_size,
                        "modified": stat.st_mtime
                    })
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied")
        
        return tree
    
    async def get_metadata(self) -> Optional[Dict]:
        """获取元数据"""
        try:
            if self._metadata_cache and self._metadata_hash:
                # 检查文件是否被修改
                current_hash = self._calculate_file_hash(METADATA_FILE)
                if current_hash == self._metadata_hash:
                    return self._metadata_cache
            
            async with aiofiles.open(METADATA_FILE, 'r', encoding='utf-8') as f:
                content = await f.read()
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

# 创建文件管理器实例
file_manager = FileManager(DATA_DIR)

@app.get("/")
async def root():
    """API根路径"""
    return {
        "name": "Palimpsest API",
        "version": "1.0.0",
        "data_directory": str(DATA_DIR),
        "endpoints": {
            "files": "/files",
            "search": "/search",
            "metadata": "/metadata",
            "tree": "/tree"
        }
    }

@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    """获取文件内容"""
    try:
        content = await file_manager.get_file_content(file_path)
        return JSONResponse(content={"content": content})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.head("/files/{file_path:path}")
async def get_file_info(file_path: str):
    """获取文件信息（不返回内容）"""
    try:
        info = await file_manager.get_file_info(file_path)
        return JSONResponse(content=info)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search_files(
    q: str = Query(..., description="搜索关键词"),
    limit: int = Query(100, description="返回结果数量限制")
):
    """搜索文件名"""
    if not q:
        raise HTTPException(status_code=400, detail="Search query is required")
    
    try:
        results = await file_manager.search_files(q, limit)
        return JSONResponse(content={
            "query": q,
            "results": results,
            "total": len(results)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metadata")
async def get_metadata():
    """获取元数据"""
    try:
        metadata = await file_manager.get_metadata()
        if metadata is None:
            raise HTTPException(status_code=404, detail="Metadata not found")
        return JSONResponse(content=metadata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tree")
async def get_directory_tree(path: str = Query("", description="目录路径")):
    """获取目录树结构"""
    try:
        tree = await file_manager.get_directory_tree(path)
        return JSONResponse(content=tree)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """获取统计信息"""
    try:
        metadata = await file_manager.get_metadata()
        if metadata:
            return JSONResponse(content={
                "total_files": metadata.get("total_files", 0),
                "total_size": metadata.get("total_size", 0),
                "scan_time": metadata.get("scan_time", ""),
                "data_directory": str(DATA_DIR)
            })
        else:
            # 如果没有元数据，计算基本统计
            total_files = 0
            total_size = 0
            
            for root, dirs, files in os.walk(DATA_DIR):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        stat = file_path.stat()
                        total_files += 1
                        total_size += stat.st_size
                    except (OSError, PermissionError):
                        continue
            
            return JSONResponse(content={
                "total_files": total_files,
                "total_size": round(total_size / 1024, 2),  # KB
                "data_directory": str(DATA_DIR)
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # 检查数据目录
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")
    
    print(f"Starting Palimpsest API server...")
    print(f"Data directory: {DATA_DIR.absolute()}")
    print(f"API documentation: http://localhost:8000/docs")
    print(f"Server running on http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)