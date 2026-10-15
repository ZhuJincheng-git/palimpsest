# Palimpsest 使用指南

## 项目概述

Palimpsest 是一个个人数据分析和洞见生成系统，通过深度分析用户的个人数据，提供个性化的人生经验和指导。

## 新项目结构

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

## 快速开始

### 1. 数据初始化

```bash
# 初始化数据目录监控
python data_tools/file_monitor.py data --init

# 或者使用详细模式
python data_tools/file_monitor.py data --init --verbose
```

### 2. 检查数据变化

```bash
# 检查文件改动（简洁模式）
python data_tools/file_monitor.py data --check

# 详细模式查看改动详情
python data_tools/file_monitor.py data --check --verbose
```

### 3. 更新元数据

```bash
# 更新数据监控（简洁模式）
python data_tools/file_monitor.py data --update

# 带描述的更新
python data_tools/file_monitor.py data --update --description "添加了新的日记内容"

# 详细模式
python data_tools/file_monitor.py data --update --verbose --description "分析本周数据"
```

### 4. 查看历史记录

```bash
# 查看最近5条历史记录（简洁模式）
python data_tools/file_monitor.py data --history --limit 5

# 详细模式查看历史
python data_tools/file_monitor.py data --history --limit 5 --verbose

# 查看特定文件的历史记录
python data_tools/file_monitor.py data --history --file "diary"
```

## MCP服务器功能

如果需要使用MCP服务器功能：

```bash
# 启动MCP服务器
python start.py

# 测试MCP服务器
python mcp_tools/test_mcp.py
```

## Agent工作模式

Palimpsest支持两种工作模式：

### 1. 独立Agent模式
- 无需MCP服务器
- 直接分析用户数据
- 生成个性化人生洞见
- 适合深度个人分析

### 2. MCP集成模式
- 通过MCP协议提供数据访问
- 支持多种AI客户端
- 实时数据同步
- 适合多平台协作

## 数据管理

### 数据目录结构
- `data/raw/`: 原始数据（只读）
- `data/insights/`: 分析结果和洞察
- `data/memory/`: 交互记忆和用户反馈
- `data/metadata.json`: 系统元数据

### 数据监控功能
- 自动检测文件变化
- 生成差异报告
- 维护更新历史
- 支持增量更新

## 最佳实践

1. **定期更新**: 定期运行 `--update` 保持数据最新
2. **详细记录**: 使用 `--description` 记录更新内容
3. **版本控制**: 重要数据变更前先检查状态
4. **备份意识**: 定期备份 `data/` 目录

## 故障排除

### 常见问题

1. **元数据文件丢失**
   ```bash
   python data_tools/file_monitor.py data --init
   ```

2. **权限问题**
   ```bash
   chmod +x data_tools/file_monitor.py
   ```

3. **依赖缺失**
   ```bash
   pip install -r requirements.txt
   ```

### 获取帮助

```bash
# 查看工具帮助
python data_tools/file_monitor.py --help

# 查看MCP文档
cat mcp_tools/API_README.md
```

## 高级功能

### 自定义监控
```bash
# 监控特定目录
python data_tools/file_monitor.py /path/to/your/data --init
```

### 批量操作
```bash
# 查看所有更新历史
python data_tools/file_monitor.py data --history --limit 0
```

### 数据分析
结合 `AGENT.md` 中的指导，系统可以：
- 生成个性化人生建议
- 识别行为模式和趋势
- 提供时间线分析
- 记录用户成长轨迹