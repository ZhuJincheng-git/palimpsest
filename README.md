# Palimpsest 底色

## 概述

这是一个个人数字信息档案库，用于让Agent读取并进行理解分析，帮助Agent深度理解用户，以更有深度地给用户**提供个性化建议、回答用户问题等**，在这个过程中Agent成为用户的人生反馈者/导师，构建的Agent×Human进化体。

在对话/问答过程中Agent不断进一步理解用户，并进行客观记录，用户不断增加原始数据，让Agent不断更新对用户的理解。

该信息库能够给到各种Agent使用以保证模型选择的灵活性。

## 新项目结构

```
palimpsest/
├── README.md                    # 项目主要说明
├── AGENT.md                     # Agent工作规范和输出约定
├── PROJECT_STRUCTURE.md        # 项目结构说明
├── USAGE_GUIDE.md              # 使用指南
├── requirements.txt            # Python依赖
├── .gitignore                 # Git忽略文件配置
├── run.py                     # 项目运行脚本
├── start.py                   # MCP服务器启动脚本
├── data_analysis.py           # 数据分析工具启动脚本
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

### 1. 数据管理

```bash
# 交互式数据分析工具
python3 data_analysis.py

# 直接使用文件监控工具
python3 data_tools/file_monitor.py data --check          # 检查变化
python3 data_tools/file_monitor.py data --init          # 初始化
python3 data_tools/file_monitor.py data --update        # 更新
python3 data_tools/file_monitor.py data --history       # 查看历史
```

### 2. MCP服务器（可选）

```bash
# 启动MCP服务器
python3 start.py

# 测试MCP服务器
python3 mcp_tools/test_mcp.py
```

## 工作模式

### 独立Agent模式
- 无需MCP服务器
- 直接分析用户数据
- 生成个性化人生洞见
- 适合深度个人分析

### MCP集成模式
- 通过MCP协议提供数据访问
- 支持多种AI客户端
- 实时数据同步
- 适合多平台协作

## 核心功能

- 📊 **数据监控**: 自动检测文件变化，生成差异报告
- 🔍 **深度分析**: 基于用户数据生成个性化洞见
- 📈 **历史追踪**: 维护数据更新历史，支持版本对比
- 💡 **个性化建议**: 基于真实数据提供人生指导
- 🔄 **增量更新**: 支持数据增量更新，提高效率

## 常见应用

- Agent为用户构建健康管理计划，用户上传健康数据到信息库，作为用户长期的健康管理师
- Agent指出用户思维惯性、盲点，帮助用户尽早发现问题
- Agent个性化地为用户提供人生建议/避免踩坑，基于高知/先行者帮助用户规划人生
- 用户上传大量其喜欢的图片示例，Agent深度理解用户审美偏好，帮助用户构建符合自己审美的提示词用于AIGC

## 文档

- [AGENT.md](AGENT.md) - Agent工作规范和输出约定
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细使用指南
- [mcp_tools/API_README.md](mcp_tools/API_README.md) - MCP服务器详细说明