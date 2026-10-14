# Palimpsest API Server

高性能、简洁、高质量的Python服务端，支持通过API读取data/内文件，支持全data文件名搜索。

## 特性

- 🚀 **高性能**: 使用FastAPI + 异步I/O，支持高并发
- 📁 **全格式支持**: 支持所有文件格式，无扩展名限制
- 🔍 **强大搜索**: 支持全文件名搜索，模糊匹配
- 📊 **元数据支持**: 自动读取和缓存文件元数据
- 🌐 **CORS支持**: 跨域请求支持
- 📖 **自动文档**: 自动生成API文档
- 🔧 **简洁设计**: 代码简洁，易于维护

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python start_server.py
```

或直接运行：

```bash
python api_server.py
```

### 3. 访问API

- API文档: http://localhost:8000/docs
- API根路径: http://localhost:8000/

## API接口

### 基础信息

- `GET /` - 获取API基本信息
- `GET /stats` - 获取文件统计信息

### 文件操作

- `GET /files/{file_path:path}` - 获取文件内容
- `HEAD /files/{file_path:path}` - 获取文件信息（不返回内容）

### 搜索功能

- `GET /search?q=关键词` - 搜索文件名

### 系统信息

- `GET /metadata` - 获取元数据
- `GET /tree` - 获取目录树结构

## 使用示例

### 搜索文件

```bash
curl "http://localhost:8000/search?q=简历"
```

响应示例：
```json
{
  "query": "简历",
  "results": [
    {
      "path": "raw/简历/朱金成_Web开发_简历.pdf",
      "name": "朱金成_Web开发_简历.pdf",
      "size": 154890,
      "modified": 1678886400.123
    }
  ],
  "total": 1
}
```

### 获取文件内容

```bash
curl "http://localhost:8000/files/raw/INDEX.md"
```

### 获取目录树

```bash
curl "http://localhost:8000/tree"
```

### 获取元数据

```bash
curl "http://localhost:8000/metadata"
```

## 性能特点

1. **异步处理**: 使用aiofiles进行异步文件读取
2. **缓存机制**: 元数据缓存，减少重复计算
3. **内存优化**: 流式处理大文件
4. **错误处理**: 完善的异常处理机制

## 安全考虑

- 文件访问限制在data/目录内
- 支持CORS配置
- 错误信息不暴露敏感信息
- 文件大小和类型检查

## 扩展功能

可以轻松扩展以下功能：
- 文件上传
- 用户认证
- 权限控制
- 文件压缩
- 缓存策略