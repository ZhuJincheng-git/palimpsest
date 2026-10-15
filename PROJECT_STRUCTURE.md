# Palimpsest 项目结构

```
palimpsest/
├── README.md                    # 项目主要说明
├── AGENT.md                     # Agent工作规范和输出约定
├── PROJECT_STRUCTURE.md        # 项目结构说明
├── requirements.txt            # Python依赖
├── .gitignore                 # Git忽略文件配置
├── run.py                     # 项目运行脚本
├── start.py                   # MCP服务器启动脚本
├── data/                      # 用户数据目录（Git忽略）
│   ├── raw/                   # 原始数据
│   ├── insights/              # 分析结果
│   ├── memory/                # 交互记忆
│   └── metadata.json          # 元数据
├── mcp_tools/                 # MCP相关工具和配置
│   ├── mcp_server.py          # MCP服务器核心代码
│   ├── test_mcp.py            # MCP服务器测试脚本
│   ├── API_README.md          # MCP服务器详细说明
│   └── MCP_CONFIG_EXAMPLES.md  # MCP客户端配置示例
├── data_tools/                # 数据操作工具
│   └── file_monitor.py        # 文件监控工具
└── .git/                     # Git版本控制
```

## 核心文件说明

### 主要脚本
- **run.py**: 项目运行脚本，提供菜单式操作界面
- **start.py**: MCP服务器启动脚本，包含依赖检查
- **mcp_server.py**: MCP服务器核心实现，符合MCP标准协议
- **test_mcp.py**: MCP服务器功能测试脚本

### 配置和文档
- **AGENT.md**: 定义Agent的工作规范、数据访问规则和输出格式
- **API_README.md**: MCP服务器的详细使用说明和API文档
- **MCP_CONFIG_EXAMPLES.md**: 各种AI客户端的MCP配置示例
- **requirements.txt**: Python依赖列表

### 工具和系统
- **file_monitor.py**: 文件监控工具，用于检测数据变化
- **data/**: 用户数据目录，包含个人档案的所有数据

## 使用方法

### 1. 快速启动
```bash
python run.py
```

### 2. 直接启动MCP服务器
```bash
python start.py
```

### 3. 运行测试
```bash
python test_mcp.py
```

### 4. 配置AI客户端
参考 `MCP_CONFIG_EXAMPLES.md` 配置支持MCP的AI客户端。

## 功能特性

### MCP服务器功能
- 📁 文件树查询（支持多层递归）
- 📄 文件读取和列表
- 🔍 全文搜索
- 📊 文件信息获取
- 📈 系统元数据

### 系统特性
- 🔒 安全的文件访问控制
- ⚡ 异步处理，高性能
- 🛡️ 防止路径遍历攻击
- 📊 智能缓存机制

## 开发环境

- Python 3.8+
- MCP 依赖
- Git 版本控制

## 数据管理

用户数据存储在 `data/` 目录下，包含：
- **raw/**: 原始数据（只读）
- **insights/**: 分析结果
- **memory/**: 交互记忆
- **metadata.json**: 系统元数据

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License