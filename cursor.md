## 项目背景

这个是一个跑通agent行业模型的项目产品，目前先考虑金融行业模型，比如股票咨询这个细分场景。产品的定位是用户问产品某某股票怎么样，agent来回答。

## 核心需求

- **部署环境**：RTX 3070 8GB显卡
- **架构模式**：服务端-客户端架构，Agent在有显卡的机器作为服务运行，局域网内其他机器通过CLI/API访问
- **数据来源**：初期使用模拟数据/历史数据（akshare），后期可接入真实API

## 技术框架设计

### 1. 核心技术栈

| 组件 | 技术选型 | 说明 |
|------|---------|------|
| **LLM模型** | ChatGLM3-6B INT4 | 4GB显存，15-20 tokens/s，中文金融能力强 |
| **Agent框架** | LangGraph + LangChain | 灵活的状态图管理，原生支持工具调用 |
| **向量模型** | bge-small-zh-v1.5 | <500MB显存，中文金融文本 |
| **向量数据库** | Chroma | 轻量级本地部署 |
| **API服务** | FastAPI | 异步高性能，支持WebSocket |
| **数据源** | akshare | 开源免费，获取A股历史数据 |
| **服务端口** | 8765 | 避免常用端口冲突 |

### 2. 系统架构

```
[客户端机器] --HTTP/WebSocket--> [FastAPI服务:8765]
                                      ↓
                                [LangGraph Agent]
                        ↙          ↓           ↘
                [ChatGLM3-6B]  [工具集]  [RAG检索器]
                                  ↓           ↓
                            [股票数据]  [Chroma向量库]
```

### 3. Agent工作流（ReAct模式）

1. **意图识别** → 理解用户查询（如"比亚迪怎么样？"）
2. **工具选择** → 决定调用哪些工具（价格查询、财务指标等）
3. **工具执行** → 调用LangChain工具获取数据
4. **知识检索** → 从RAG知识库获取相关金融知识
5. **综合分析** → LLM基于数据和知识生成投资建议
6. **流式输出** → 通过SSE/WebSocket返回给客户端

### 4. 五大核心工具

1. `get_stock_price` - 获取历史价格数据
2. `get_financial_indicators` - 获取财务指标（PE、ROE等）
3. `calculate_technical_indicators` - 计算技术指标（MA、MACD、RSI）
4. `search_stock_news` - 搜索相关新闻
5. `compare_stocks` - 对比多只股票

### 5. RAG知识库

**数据来源**：
- 金融术语词典（百度百科API爬取）
- 基础知识文档（手工编写，项目内置）
- A股规则文档（证监会官网PDF）
- 技术分析教程（开源教材）
- 常见问答对（模板生成）

### 6. 预置数据

- **股票数据**：50只热门A股历史数据（2020-2024，parquet格式，~20MB）
- **知识库**：800KB markdown文件
- **提供脚本**：`download_stock_data.py`、`crawl_finance_terms.py`、`build_vectordb.py`

### 7. 部署方案

支持三种迁移方式：
1. **Docker镜像**（推荐）- 一键打包和加载
2. **Conda环境** - 环境导出和还原
3. **安装脚本** - Windows PowerShell / Linux Bash自动化安装

### 8. 测试体系

- **单元测试**：工具函数、数据加载、RAG检索（pytest + coverage）
- **集成测试**：Agent工作流、API端点（FastAPI TestClient）
- **压力测试**：并发性能测试（Locust）
- **目标覆盖率**：工具>90%，核心逻辑>80%，API>85%

### 9. 性能预估

- 模型加载：15-20秒
- 首Token延迟：0.8-1.5秒
- 生成速度：15-20 tokens/s
- 并发支持：3-4人流畅
- 显存占用：4.5-5.5GB

### 10. 客户端使用

```bash
# 安装客户端
pip install ./client

# 配置服务端
stock-agent config --server http://192.168.1.100:8765 --token xxx

# 使用
stock-agent chat                          # 交互式对话
stock-agent query "比亚迪怎么样？"         # 单次查询
stock-agent batch stocks.txt -o report.md # 批量分析
```