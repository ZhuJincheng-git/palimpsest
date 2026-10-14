#!/usr/bin/env python3
"""
API客户端示例
"""

import requests
import json
from typing import Dict, List

class PalimpsestAPIClient:
    """Palimpsest API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def search_files(self, query: str, limit: int = 100) -> Dict:
        """搜索文件"""
        response = requests.get(f"{self.base_url}/search", params={"q": query, "limit": limit})
        response.raise_for_status()
        return response.json()
    
    def get_file_content(self, file_path: str) -> str:
        """获取文件内容"""
        response = requests.get(f"{self.base_url}/files/{file_path}")
        response.raise_for_status()
        return response.json()["content"]
    
    def get_file_info(self, file_path: str) -> Dict:
        """获取文件信息"""
        response = requests.head(f"{self.base_url}/files/{file_path}")
        response.raise_for_status()
        return response.json()
    
    def get_metadata(self) -> Dict:
        """获取元数据"""
        response = requests.get(f"{self.base_url}/metadata")
        response.raise_for_status()
        return response.json()
    
    def get_directory_tree(self, path: str = "") -> Dict:
        """获取目录树"""
        response = requests.get(f"{self.base_url}/tree", params={"path": path})
        response.raise_for_status()
        return response.json()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        response = requests.get(f"{self.base_url}/stats")
        response.raise_for_status()
        return response.json()

def main():
    """客户端示例使用"""
    client = PalimpsestAPIClient()
    
    print("=== Palimpsest API 客户端示例 ===")
    
    try:
        # 获取统计信息
        stats = client.get_stats()
        print(f"\n文件统计:")
        print(f"  总文件数: {stats['total_files']}")
        print(f"  总大小: {stats['total_size']} KB")
        
        # 搜索文件
        search_results = client.search_files("INDEX")
        print(f"\n搜索 'INDEX' 结果:")
        print(f"  找到 {search_results['total']} 个文件")
        
        # 显示前3个结果
        for result in search_results['results'][:3]:
            print(f"    - {result['path']}")
        
        # 获取文件内容
        if search_results['results']:
            first_file = search_results['results'][0]['path']
            content = client.get_file_content(first_file)
            print(f"\n文件 '{first_file}' 内容预览:")
            print(f"  长度: {len(content)} 字符")
            print(f"  前100字符: {content[:100]}...")
        
        # 获取目录树
        tree = client.get_directory_tree()
        print(f"\n目录树结构:")
        print(f"  根目录包含 {len(tree['children'])} 个项目")
        
        # 显示前5个子项
        for child in tree['children'][:5]:
            print(f"    - {child['name']} ({child['type']})")
    
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()