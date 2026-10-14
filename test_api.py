#!/usr/bin/env python3
"""
API测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    """测试API功能"""
    print("=== Palimpsest API 测试 ===")
    
    # 测试基础信息
    print("\n1. 测试基础信息...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ 基础信息: {response.json()['name']}")
    except Exception as e:
        print(f"✗ 基础信息测试失败: {e}")
        return False
    
    # 测试统计信息
    print("\n2. 测试统计信息...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        stats = response.json()
        print(f"✓ 文件总数: {stats['total_files']}")
        print(f"✓ 总大小: {stats['total_size']} KB")
    except Exception as e:
        print(f"✗ 统计信息测试失败: {e}")
        return False
    
    # 测试搜索功能
    print("\n3. 测试搜索功能...")
    try:
        response = requests.get(f"{BASE_URL}/search?q=INDEX")
        results = response.json()
        print(f"✓ 搜索结果: {results['total']} 个文件")
        if results['results']:
            print(f"  示例: {results['results'][0]['path']}")
    except Exception as e:
        print(f"✗ 搜索测试失败: {e}")
        return False
    
    # 测试文件获取
    print("\n4. 测试文件获取...")
    try:
        response = requests.get(f"{BASE_URL}/files/INDEX.md")
        content = response.json()
        print(f"✓ 文件内容长度: {len(content['content'])}")
    except Exception as e:
        print(f"✗ 文件获取测试失败: {e}")
        return False
    
    # 测试目录树
    print("\n5. 测试目录树...")
    try:
        response = requests.get(f"{BASE_URL}/tree")
        tree = response.json()
        print(f"✓ 根目录包含 {len(tree['children'])} 个项目")
    except Exception as e:
        print(f"✗ 目录树测试失败: {e}")
        return False
    
    print("\n=== 所有测试通过 ===")
    return True

def test_performance():
    """性能测试"""
    print("\n=== 性能测试 ===")
    
    # 测试搜索性能
    start_time = time.time()
    for i in range(10):
        requests.get(f"{BASE_URL}/search?q=INDEX")
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 10
    print(f"✓ 搜索平均响应时间: {avg_time:.3f} 秒")
    
    # 测试文件读取性能
    start_time = time.time()
    for i in range(5):
        requests.get(f"{BASE_URL}/files/INDEX.md")
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 5
    print(f"✓ 文件读取平均响应时间: {avg_time:.3f} 秒")

if __name__ == "__main__":
    if test_api():
        test_performance()
    else:
        print("API测试失败，请确保服务器正在运行")