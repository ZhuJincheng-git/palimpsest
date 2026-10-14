#!/usr/bin/env python3
import os
import json
import hashlib
import argparse
import time
from datetime import datetime
from pathlib import Path
import sys

class FileMonitor:
    def __init__(self, directory="data/", metadata_file="metadata.json"):
        self.directory = Path(directory)
        self.metadata_file = self.directory / metadata_file
        self.supported_extensions = {'.txt', '.json', '.csv', '.xml', '.md', '.py', '.js', '.html', '.css', '.jpg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls', '.xlsx'}
    
    CHUNK_SIZE = 1024 * 1024  # 1MB分块：/mnt/e等网络文件系统上大幅减少系统调用

    def calculate_file_hash(self, file_path):
        """计算文件的SHA256哈希值"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(self.CHUNK_SIZE), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except (IOError, OSError):
            return None
    
    def get_file_metadata(self, file_path):
        """获取文件元数据"""
        try:
            stat = file_path.stat()
            return {
                'path': str(file_path.relative_to(self.directory)),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'created': stat.st_ctime,
                'hash': self.calculate_file_hash(file_path),
                'extension': file_path.suffix.lower(),
                'is_directory': file_path.is_dir()
            }
        except (OSError, ValueError):
            return None
    
    def scan_directory(self):
        """扫描目录并返回所有文件元数据"""
        metadata = {
            'scan_time': datetime.now().isoformat(),
            'directory': str(self.directory),
            'files': [],
            'total_files': 0,
            'total_size': 0
        }
        
        if not self.directory.exists():
            raise FileNotFoundError(f"目录不存在: {self.directory}")
        
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                file_path = Path(root) / file
                if file_path.name != self.metadata_file.name:
                    file_meta = self.get_file_metadata(file_path)
                    if file_meta:
                        metadata['files'].append(file_meta)
                        metadata['total_files'] += 1
                        metadata['total_size'] += file_meta['size']
        
        metadata['total_size'] = round(metadata['total_size'] / 1024, 2)  # 转换为KB
        return metadata
    
    def initialize_metadata(self):
        """初始化元数据文件"""
        print(f"正在扫描目录: {self.directory}")
        metadata = self.scan_directory()
        
        # 计算元数据的哈希值
        metadata_copy = metadata.copy()
        metadata_copy.pop('hash', None)  # 移除可能存在的hash字段
        metadata_str = json.dumps(metadata_copy, sort_keys=True)
        metadata['hash'] = hashlib.sha256(metadata_str.encode()).hexdigest()
        
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"元数据文件已生成: {self.metadata_file}")
            print(f"扫描完成: {metadata['total_files']} 个文件, 总大小: {metadata['total_size']} KB")
        except IOError as e:
            print(f"写入元数据文件失败: {e}")
            return False
        
        return True
    
    def load_metadata(self):
        """加载元数据文件"""
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"加载元数据文件失败: {e}")
            return None
    
    def compare_metadata(self, old_metadata, new_metadata):
        """比较两个元数据文件并返回差异"""
        differences = {
            'added': [],
            'deleted': [],
            'modified': [],
            'unchanged': 0,
            'scan_time': datetime.now().isoformat()
        }
        
        old_files = {f['path']: f for f in old_metadata['files']}
        new_files = {f['path']: f for f in new_metadata['files']}
        
        # 检查新增文件
        for path, new_file in new_files.items():
            if path not in old_files:
                differences['added'].append(new_file)
        
        # 检查删除文件
        for path, old_file in old_files.items():
            if path not in new_files:
                differences['deleted'].append(old_file)
        
        # 检查修改文件
        for path, new_file in new_files.items():
            if path in old_files:
                old_file = old_files[path]
                if (old_file['size'] != new_file['size'] or 
                    old_file['modified'] != new_file['modified'] or
                    old_file['hash'] != new_file['hash']):
                    differences['modified'].append({
                        'path': path,
                        'old': old_file,
                        'new': new_file
                    })
                else:
                    differences['unchanged'] += 1
        
        return differences
    
    def check_differences(self):
        """检查差异"""
        if not self.metadata_file.exists():
            print("元数据文件不存在，请先运行初始化")
            return False
        
        old_metadata = self.load_metadata()
        if not old_metadata:
            return False
        
        print("正在扫描当前目录...")
        new_metadata = self.scan_directory()
        
        # 验证旧元数据的哈希值
        old_metadata_copy = old_metadata.copy()
        old_hash = old_metadata_copy.pop('hash', None)
        metadata_str = json.dumps(old_metadata_copy, sort_keys=True)
        calculated_hash = hashlib.sha256(metadata_str.encode()).hexdigest()
        
        if old_hash != calculated_hash:
            print("警告: 元数据文件可能被篡改!")
            print(f"记录的哈希: {old_hash}")
            print(f"计算的哈希: {calculated_hash}")
        
        differences = self.compare_metadata(old_metadata, new_metadata)
        
        print("\n=== 差异报告 ===")
        print(f"扫描时间: {differences['scan_time']}")
        print(f"未变更文件: {differences['unchanged']}")
        
        if differences['added']:
            print(f"\n新增文件 ({len(differences['added'])}):")
            for file in differences['added']:
                print(f"  + {file['path']} ({file['size']} B)")

        if differences['deleted']:
            print(f"\n删除文件 ({len(differences['deleted'])}):")
            for file in differences['deleted']:
                print(f"  - {file['path']} ({file['size']} B)")

        if differences['modified']:
            print(f"\n修改文件 ({len(differences['modified'])}):")
            for file in differences['modified']:
                print(f"  * {file['path']}")
                print(f"    大小: {file['old']['size']} B -> {file['new']['size']} B")
                print(f"    修改时间: {datetime.fromtimestamp(file['old']['modified']).strftime('%Y-%m-%d %H:%M:%S')} -> {datetime.fromtimestamp(file['new']['modified']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        return differences
    
    @staticmethod
    def _fmt_time(ts):
        """时间戳格式化为可读字符串"""
        if not ts:
            return '?'
        try:
            return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
        except (OSError, OverflowError, ValueError):
            return '?'

    def show_history(self, limit=20, verbose=False, file_filter=''):
        """查看更新历史"""
        if not self.metadata_file.exists():
            print("元数据文件不存在，请先运行 --init")
            return False

        metadata = self.load_metadata()
        if not metadata:
            return False

        history = metadata.get('update_history', [])
        if not history:
            print("暂无更新历史")
            return True

        # 可选：只看涉及某路径的记录（精确或包含匹配）
        if file_filter:
            def touches(entry):
                diff = entry.get('differences', {})
                paths = ([f['path'] for f in diff.get('added', [])] +
                         [f['path'] for f in diff.get('deleted', [])] +
                         [f['path'] for f in diff.get('modified', [])])
                return any(p == file_filter or file_filter in p for p in paths)
            history = [e for e in history if touches(e)]
            if not history:
                print(f"无涉及 {file_filter} 的历史记录")
                return True

        total = len(history)
        shown = history[-limit:] if limit else history

        print("=== 更新历史 ===")
        print(f"元数据: {self.metadata_file}")
        print(f"共 {total} 条记录，显示 {len(shown)} 条")
        print()

        for i, entry in enumerate(shown):
            idx = total - len(shown) + i + 1
            diff = entry.get('differences', {})
            print(f"[{idx}] {entry.get('update_time', '?')}")
            print(f"  说明: {entry.get('description') or '(未填)'}")
            print(f"  新增 {len(diff.get('added', []))} / 删除 {len(diff.get('deleted', []))} "
                  f"/ 修改 {len(diff.get('modified', []))} / 未变更 {diff.get('unchanged', 0)}")
            if verbose:
                for f in diff.get('added', []):
                    print(f"    + {f['path']} ({f.get('size', '?')} B)")
                for f in diff.get('deleted', []):
                    print(f"    - {f['path']} ({f.get('size', '?')} B)")
                for m in diff.get('modified', []):
                    o, n = m.get('old', {}), m.get('new', {})
                    print(f"    * {m['path']}")
                    print(f"        大小: {o.get('size', '?')} B -> {n.get('size', '?')} B")
                    print(f"        时间: {self._fmt_time(o.get('modified'))} -> {self._fmt_time(n.get('modified'))}")
            print()

        return True

    def update_metadata(self, description=""):
        """更新元数据文件"""
        if not self.metadata_file.exists():
            print("元数据文件不存在，请先运行初始化")
            return False
        
        old_metadata = self.load_metadata()
        if not old_metadata:
            return False
        
        print("正在扫描当前目录...")
        new_metadata = self.scan_directory()
        
        # 生成更新说明
        update_info = {
            'update_time': datetime.now().isoformat(),
            'description': description or "自动更新",
            'previous_hash': old_metadata.get('hash', ''),
            'differences': self.compare_metadata(old_metadata, new_metadata)
        }
        
        # 创建新的元数据（先写入更新历史，再计算哈希，保证校验时全文一致）
        new_metadata['update_history'] = old_metadata.get('update_history', [])
        new_metadata['update_history'].append(update_info)
        metadata_copy = new_metadata.copy()
        metadata_str = json.dumps(metadata_copy, sort_keys=True)
        new_metadata['hash'] = hashlib.sha256(metadata_str.encode()).hexdigest()
        
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(new_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"元数据文件已更新: {self.metadata_file}")
            print(f"更新说明: {description or '自动更新'}")
            print(f"更新时间: {update_info['update_time']}")
            
            # 显示更新统计
            diff = update_info['differences']
            print(f"\n更新统计:")
            print(f"  新增文件: {len(diff['added'])}")
            print(f"  删除文件: {len(diff['deleted'])}")
            print(f"  修改文件: {len(diff['modified'])}")
            print(f"  未变更文件: {diff['unchanged']}")
            
            return True
        except IOError as e:
            print(f"更新元数据文件失败: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="文件监控和差异对比工具")
    parser.add_argument('directory', nargs='?', default='data/', help='监控目录 (默认: data/)')
    parser.add_argument('--init', action='store_true', help='初始化元数据')
    parser.add_argument('--check', action='store_true', help='检查差异')
    parser.add_argument('--update', action='store_true', help='更新元数据')
    parser.add_argument('--history', action='store_true', help='查看更新历史')
    parser.add_argument('--limit', type=int, default=20, help='--history 显示条数 (默认 20，0=全部)')
    parser.add_argument('--verbose', action='store_true', help='--history 展开文件明细')
    parser.add_argument('--file', type=str, default='', help='--history 只看涉及某路径的记录')
    parser.add_argument('--description', type=str, default='', help='更新说明')
    parser.add_argument('--metadata', type=str, default='metadata.json', help='元数据文件名')
    
    args = parser.parse_args()
    
    try:
        monitor = FileMonitor(args.directory, args.metadata)
        
        if args.init:
            success = monitor.initialize_metadata()
            sys.exit(0 if success else 1)
        elif args.check:
            success = monitor.check_differences()
            sys.exit(0 if success else 1)
        elif args.update:
            success = monitor.update_metadata(args.description)
            sys.exit(0 if success else 1)
        elif args.history:
            success = monitor.show_history(args.limit, args.verbose, args.file)
            sys.exit(0 if success else 1)
        else:
            print("请指定操作: --init, --check, --update, 或 --history")
            parser.print_help()
            sys.exit(1)
            
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()