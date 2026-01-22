# 股票咨询Agent系统 🚀

**版本**: v1.0.0 ✅  
**状态**: 开发完成，可立即使用  
**更新**: 2026-01-21  

> 一个基于LLM的智能股票咨询Agent系统，支持49只热门A股实时分析、金融知识问答、局域网多用户访问。

---

## ⭐ 核心特性

- 📈 **真实数据**：49只A股，6年历史数据（2020-2026）
- 🤖 **智能对话**：基于LLM的自然语言交互
- 🔧 **5大工具**：价格查询、技术指标、历史数据、股票对比、综合分析
- 📚 **知识库**：金融知识RAG，支持术语解释和学习
- 🌐 **局域网服务**：服务器-客户端架构，支持多用户
- 💻 **命令行界面**：友好的CLI交互体验
- 🚀 **无GPU开发**：MockLLM支持无GPU环境开发测试

---

## 🎯 快速开始

### 1分钟体验

```bash
# 测试Agent（无需启动服务器）
python test_agent.py
# 选择2进入交互模式

# 开始提问
> 比亚迪现在多少钱？
> 什么是MACD指标？
> 对比一下比亚迪和宁德时代
```

### 5分钟完整部署

```bash
# 终端1：启动服务器
python start_server.py

# 终端2：启动客户端
python start_client.py

# 开始使用
您: 分析一下贵州茅台
Agent: 根据分析，贵州茅台...
```

---

## 📖 项目文档

### 必读文档
- 📘 [USAGE_GUIDE.md](./USAGE_GUIDE.md) - **完整使用指南**（推荐）
- 📗 [QUICKSTART.md](./QUICKSTART.md) - 快速开始
- 📙 [TOOLS_GUIDE.md](./TOOLS_GUIDE.md) - 工具使用说明

### 开发文档
- 📕 [PLAN.md](./PLAN.md) - 技术实现计划
- 📔 [STATUS.md](./STATUS.md) - 项目状态
- 📓 [tracker.md](./tracker.md) - 开发追踪
- 📚 [COMPLETED.md](./COMPLETED.md) - 完成总结

---

## 🚀 项目状态

✅ **所有功能已完成！**（8/8任务）

| 任务 | 状态 | 说明 |
|------|------|------|
| 环境搭建 | ✅ | Python环境、依赖管理 |
| 数据准备 | ✅ | 49只股票、知识库 |
| LLM服务 | ✅ | MockLLM + ChatGLM3 |
| 股票工具 | ✅ | 5个专业工具 |
| RAG系统 | ✅ | 知识库检索 |
| Agent核心 | ✅ | 智能路由、工具调用 |
| FastAPI服务 | ✅ | HTTP API（8765端口） |
| CLI客户端 | ✅ | 交互式界面 |

**总进度**: 100% 🎉

---

## 🛠️ 技术栈

- **LLM**: ChatGLM3-6B（可选Mock模式）
- **Agent框架**: LangChain + LangGraph
- **数据源**: akshare（真实市场数据）
- **Web框架**: FastAPI + Uvicorn
- **存储**: Parquet（股票数据）+ JSON（知识库）
- **Python**: 3.12+

---

## 📊 功能展示

### 支持的查询类型

1. **价格查询**
```
您: 比亚迪现在多少钱？
Agent: 【比亚迪】最新行情：收盘价94.10元，涨跌幅-0.68%...
```

2. **技术指标**
```
您: 宁德时代的技术指标怎么样？
Agent: 【宁德时代】技术指标分析：MA5: 350.88元，RSI: 26.77（超卖）...
```

3. **股票对比**
```
您: 对比一下比亚迪和宁德时代
Agent: 【股票对比】比亚迪收盘94.10元(-0.68%)，宁德时代349.81元(+0.06%)...
```

4. **知识查询**
```
您: 什么是MACD指标？
Agent: MACD是异同移动平均线，由DIF、DEA、MACD柱组成...
```

5. **综合分析**
```
您: 分析一下中国平安
Agent: 【中国平安】综合分析：收盘65.85元，RSI 18.11（超卖），趋势：弱势下跌...
```

---

## 📦 项目结构

```
c:/project/agent/
├── server/                    # 服务端
│   ├── src/
│   │   ├── agent/            # Agent核心
│   │   ├── api/              # FastAPI接口
│   │   ├── llm/              # LLM服务
│   │   ├── rag/              # RAG系统
│   │   ├── tools/            # 股票工具
│   │   └── data/             # 数据加载
│   └── configs/              # 配置文件
├── client/                    # 客户端
│   └── src/cli/              # CLI界面
├── scripts/                   # 脚本工具
├── data/                      # 数据文件
│   ├── stocks/               # 股票数据（49只）
│   └── knowledge/            # 知识库
├── test_*.py                 # 测试脚本
├── start_server.py           # 启动服务器
├── start_client.py           # 启动客户端
└── *.md                      # 文档
```

---

## 🎮 使用方式

### 方式1：独立测试（推荐新手）
```bash
python test_agent.py  # 本地测试，无需服务器
```

### 方式2：服务器-客户端（推荐团队）
```bash
# 机器A（服务器）
python start_server.py

# 机器B（客户端）
python start_client.py http://机器A的IP:8765
```

### 方式3：API调用（推荐集成）
```python
import requests
response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "比亚迪现在多少钱？"}
)
print(response.json()['answer'])
```

---

## 🧪 测试

所有测试100%通过：

```bash
python test_tools.py   # 测试5个股票工具
python test_rag.py     # 测试知识库检索
python test_agent.py   # 测试Agent核心
python test_api.py     # 测试API接口（需先启动服务器）
```

---

## 📈 数据统计

- **代码量**: ~5000行Python代码
- **文件数**: 66个（代码+配置+文档）
- **股票数**: 49只热门A股
- **数据量**: 68,600+条历史记录
- **知识库**: 21个文档块
- **时间跨度**: 2020-2026（6年）

---

## ❓ 常见问题

**Q: 需要GPU吗？**  
A: 不需要！默认使用MockLLM，无GPU也能运行。

**Q: 支持哪些股票？**  
A: 49只热门A股，包括比亚迪、宁德时代、贵州茅台等。运行 `python start_client.py` 后输入 `/stocks` 查看完整列表。

**Q: 如何添加更多股票？**  
A: 修改 `scripts/download_stock_data.py`，添加股票代码，重新运行下载脚本。

**Q: 局域网如何使用？**  
A: 服务器运行 `python start_server.py`，客户端运行 `python start_client.py http://服务器IP:8765`

**Q: 数据多久更新？**  
A: 当前是静态数据（截至2026-01-21），可定时运行 `python scripts/download_stock_data.py` 更新。

更多问题请查看 [USAGE_GUIDE.md](./USAGE_GUIDE.md)

---

## 🔧 配置

编辑 `server/configs/server_config.yaml`：

```yaml
model:
  mock_mode: true    # false使用真实GPU模型
  device: cuda       # 或cpu
  path: ./models/chatglm3-6b

server:
  host: 0.0.0.0     # 监听所有IP
  port: 8765        # 服务端口
```

---

## 🚀 下一步

1. **立即体验**: `python test_agent.py`
2. **阅读文档**: [USAGE_GUIDE.md](./USAGE_GUIDE.md)
3. **部署服务**: `python start_server.py`
4. **连接客户端**: `python start_client.py`

---

## 📄 许可

仅供学习和研究使用。数据来源：akshare（公开数据）。

**投资有风险，入市需谨慎。本系统不构成任何投资建议。**

---

## 🎉 致谢

感谢以下开源项目：
- ChatGLM3-6B（清华KEG）
- LangChain & LangGraph
- FastAPI
- akshare

---

**开始使用吧！** 🚀📈💰

更多信息请查看 [USAGE_GUIDE.md](./USAGE_GUIDE.md)
