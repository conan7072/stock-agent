# 股票咨询Agent系统 🚀

基于LangGraph和ChatGLM的智能股票分析AI Agent，支持实时数据查询、技术指标分析、知识问答。

[![GitHub](https://img.shields.io/badge/GitHub-conan7072%2Fstock--agent-blue)](https://github.com/conan7072/stock-agent)
[![Docker](https://img.shields.io/badge/Docker-支持-2496ED?logo=docker)](https://github.com/conan7072/stock-agent/blob/main/DOCKER_GUIDE.md)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)

---

## ✨ 核心特性

- 📈 **真实数据**：50只A股热门股票，6年历史数据
- 🤖 **智能对话**：基于LLM的自然语言交互
- 🔧 **5大工具**：价格查询、技术指标、历史数据、股票对比、综合分析
- 📚 **知识库**：金融术语RAG检索
- 🐳 **Docker部署**：一键启动，支持Mock/GPU模式
- 🌐 **API接口**：FastAPI RESTful服务
- 💻 **CLI客户端**：友好的命令行界面

---

## 🚀 快速开始

### 方式1：Docker部署（推荐）

```bash
# 使用Mock模式（无需GPU）
docker build --build-arg MODE=mock -t stock-agent:mock .
docker run -d -p 8765:8765 stock-agent:mock

# 访问API文档
http://localhost:8765/docs
```

### 方式2：从源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent

# 2. 安装依赖
pip install -r requirements.txt
pip install -r server/requirements.txt

# 3. 下载数据
python scripts/download_stock_data.py
python scripts/convert_index.py

# 4. 启动服务
python start_server.py

# 5. 启动客户端（另一个终端）
python start_client.py
```

---

## 💬 使用示例

### API调用

```python
import requests

response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "比亚迪现在多少钱？"}
)
print(response.json()['answer'])
```

### CLI交互

```bash
$ python start_client.py

欢迎使用股票咨询Agent！

您: 比亚迪现在多少钱？
Agent: 【比亚迪(002594)】最新行情：
- 收盘价: 94.10元
- 涨跌幅: -0.68%
- 成交量: 123,456手
...

您: 什么是MACD指标？
Agent: MACD（异同移动平均线）是技术分析中的趋势指标...
```

---

## 🛠️ 技术栈

- **Agent框架**: LangChain + LangGraph
- **LLM**: ChatGLM3-6B / Mock模式
- **Web框架**: FastAPI + Uvicorn
- **数据源**: akshare（A股实时数据）
- **存储**: Parquet + JSON
- **部署**: Docker + docker-compose

---

## 📦 Docker部署

### Mock模式（无GPU）

```bash
# 构建
docker build --build-arg MODE=mock -t stock-agent:mock .

# 启动
docker-compose --profile mock up -d

# 查看日志
docker-compose logs -f agent-mock
```

### GPU模式（ChatGLM3）

```bash
# 1. 下载模型
python scripts/download_model.py --model chatglm3-6b-int4

# 2. 修改配置 server/configs/server_config.yaml
#    设置 mock_mode: false

# 3. 构建并启动
docker build --build-arg MODE=gpu -t stock-agent:chatglm3 .
docker-compose --profile chatglm3 up -d
```

**详细文档**: [DOCKER_GUIDE.md](./DOCKER_GUIDE.md)

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [QUICKSTART.md](./QUICKSTART.md) | 快速开始指南 |
| [USAGE_GUIDE.md](./USAGE_GUIDE.md) | 完整使用指南 |
| [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) | Docker部署指南 |
| [MODEL_GUIDE.md](./MODEL_GUIDE.md) | 模型选择指南 |
| [TOOLS_GUIDE.md](./TOOLS_GUIDE.md) | 工具使用说明 |

---

## 🎯 功能展示

### 支持的查询类型

| 类型 | 示例 |
|------|------|
| **价格查询** | "比亚迪现在多少钱？" |
| **技术指标** | "宁德时代的MACD怎么样？" |
| **历史数据** | "比亚迪最近一个月走势" |
| **股票对比** | "比较比亚迪和宁德时代" |
| **综合分析** | "分析一下贵州茅台" |
| **知识问答** | "什么是RSI指标？" |

---

## 📊 API接口

### 端点列表

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/chat` | POST | 聊天查询 |
| `/tools` | GET | 工具列表 |
| `/stocks` | GET | 股票列表 |

**API文档**: 启动服务后访问 http://localhost:8765/docs

---

## ⚙️ 配置

编辑 `server/configs/server_config.yaml`：

```yaml
model:
  mock_mode: true          # false使用真实GPU模型
  name: chatglm3-6b
  device: cuda
  path: ./models/chatglm3-6b

server:
  host: 0.0.0.0
  port: 8765
```

---

## 🔧 支持的股票

包含50只A股热门股票：

- **科技**: 比亚迪、宁德时代、海康威视、立讯精密...
- **消费**: 贵州茅台、五粮液、伊利股份、海天味业...
- **金融**: 招商银行、中国平安、工商银行、建设银行...
- **更多**: 查看 `/stocks` API或运行客户端输入 `/stocks`

---

## 📈 数据说明

- **数据来源**: akshare公开数据
- **更新频率**: 手动更新（运行 `python scripts/download_stock_data.py`）
- **时间跨度**: 2020-2026（约6年）
- **数据量**: 68,000+条历史记录

---

## ❓ 常见问题

**Q: 需要GPU吗？**  
A: 不需要。默认Mock模式无需GPU，适合开发测试。

**Q: 如何切换到真实LLM？**  
A: 下载模型后，修改配置文件 `mock_mode: false`。

**Q: 支持哪些显卡？**  
A: RTX 3060 6GB以上（推荐RTX 3070 8GB）。

**Q: 如何添加更多股票？**  
A: 编辑 `scripts/download_stock_data.py`，添加股票代码后重新运行。

**Q: 可以商用吗？**  
A: 仅供学习研究使用。

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可

MIT License

**投资有风险，入市需谨慎。本系统不构成任何投资建议。**

---

## 🎉 致谢

- [ChatGLM3-6B](https://github.com/THUDM/ChatGLM3) - 清华KEG实验室
- [LangChain](https://github.com/langchain-ai/langchain) - Agent框架
- [akshare](https://github.com/akfamily/akshare) - 金融数据接口
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架

---

**开始使用** → [快速开始指南](./QUICKSTART.md)
