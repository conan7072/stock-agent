# 股票咨询Agent系统 🚀

基于LangGraph和ChatGLM的智能股票分析AI Agent，支持实时数据查询、技术指标分析、知识问答。

[![GitHub](https://img.shields.io/badge/GitHub-conan7072%2Fstock--agent-blue)](https://github.com/conan7072/stock-agent)
[![Docker](https://img.shields.io/badge/Docker-支持-2496ED?logo=docker)](https://github.com/conan7072/stock-agent/blob/main/DOCKER_GUIDE.md)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)

---

## ✨ 特性

- 📈 **真实数据**：50只A股热门股票，6年历史数据
- 🤖 **智能对话**：基于LLM的自然语言交互
- 🔧 **5大工具**：价格查询、技术指标、历史数据、股票对比、综合分析
- 📚 **知识库**：金融术语RAG检索
- 🐳 **Docker部署**：一键启动，支持Mock/GPU模式
- 🌐 **API接口**：FastAPI RESTful服务

---

## 🚀 快速开始（3步）

### 步骤1：获取代码

```bash
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent
```

### 步骤2：安装依赖

```bash
pip install -r requirements.txt
pip install -r server/requirements.txt
pip install -r client/requirements.txt
```

### 步骤3：准备数据

```bash
# 下载股票数据
python scripts/download_stock_data.py

# 构建知识库索引
python scripts/convert_index.py
```

### 步骤4：启动服务

```bash
# 启动服务端（Mock模式，无需GPU）
python start_server.py
```

**服务已启动！** 访问 http://localhost:8765/docs 查看API文档

---

## 💬 使用方式

### 方式1：命令行客户端（推荐新手）

```bash
# 新开一个终端，启动客户端
python start_client.py

# 开始对话
您: 比亚迪现在多少钱？
Agent: 【比亚迪(002594)】最新行情：收盘价94.10元...

您: 什么是MACD指标？
Agent: MACD是异同移动平均线，用于判断趋势...

您: exit  # 退出
```

### 方式2：API调用（推荐开发者）

```python
import requests

# 发送查询
response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "比亚迪现在多少钱？"}
)

# 获取结果
print(response.json()['answer'])
```

### 方式3：浏览器测试（推荐快速体验）

访问 **http://localhost:8765/docs**

在Swagger UI中测试所有API：
1. 点击 `POST /chat`
2. 点击 "Try it out"
3. 输入问题：`{"query": "比亚迪现在多少钱？"}`
4. 点击 "Execute"

---

## 🐳 Docker部署（推荐生产环境）

### Mock模式（无需GPU）

```bash
# 一键启动
docker-compose --profile mock up -d

# 查看日志
docker-compose logs -f agent-mock

# 访问服务
curl http://localhost:8765/health
```

### GPU模式（ChatGLM3-6B）

```bash
# 1. 下载模型（需要等待）
python scripts/download_model.py --model chatglm3-6b-int4

# 2. 修改配置
# 编辑 server/configs/server_config.yaml
# 设置 mock_mode: false

# 3. 启动GPU版本（需要NVIDIA Docker）
docker-compose --profile chatglm3 up -d
```

**详细文档**: [DOCKER_GUIDE.md](./DOCKER_GUIDE.md)

---

## 📖 查询示例

| 查询类型 | 示例问题 |
|---------|---------|
| **价格查询** | "比亚迪现在多少钱？" |
| **技术指标** | "宁德时代的MACD怎么样？" |
| **历史数据** | "比亚迪最近一个月走势" |
| **股票对比** | "比较比亚迪和宁德时代" |
| **综合分析** | "分析一下贵州茅台" |
| **知识问答** | "什么是RSI指标？" |

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [QUICKSTART.md](./QUICKSTART.md) | 详细的快速开始指南 |
| [USAGE_GUIDE.md](./USAGE_GUIDE.md) | 完整使用手册 |
| [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) | Docker部署完全指南 |
| [MODEL_GUIDE.md](./MODEL_GUIDE.md) | 模型选择和配置 |
| [TOOLS_GUIDE.md](./TOOLS_GUIDE.md) | 5个工具详细说明 |

---

## 🛠️ 技术架构

```
┌─────────────┐
│   客户端     │  (CLI / API / 浏览器)
└──────┬──────┘
       │ HTTP
┌──────▼──────┐
│  FastAPI    │  (端口8765)
└──────┬──────┘
       │
┌──────▼──────┐
│ LangGraph   │  (Agent核心)
│   Agent     │
└──┬───┬───┬──┘
   │   │   │
   │   │   └────► RAG检索 (知识库)
   │   └────────► LLM (ChatGLM3/Mock)
   └────────────► 工具集 (5个股票工具)
                  └─► 数据源 (Parquet文件)
```

**技术栈**:
- Agent: LangChain + LangGraph
- LLM: ChatGLM3-6B (可选Mock)
- Web: FastAPI + Uvicorn
- 数据: akshare + Parquet

---

## ⚙️ 配置

编辑 `server/configs/server_config.yaml`：

```yaml
# 模型配置
model:
  mock_mode: true          # false=使用真实GPU模型
  name: chatglm3-6b
  device: cuda             # cuda/cpu
  path: ./models/chatglm3-6b

# 服务配置
server:
  host: 0.0.0.0           # 监听所有IP
  port: 8765              # 服务端口
```

---

## 🔧 支持的股票

**50只A股热门股票**：

- **新能源**: 比亚迪、宁德时代、天齐锂业、赣锋锂业...
- **白酒**: 贵州茅台、五粮液、泸州老窖、山西汾酒...
- **科技**: 海康威视、立讯精密、京东方A...
- **金融**: 招商银行、中国平安、工商银行...
- **医药**: 恒瑞医药、药明康德、迈瑞医疗...

**查看完整列表**: 运行客户端后输入 `/stocks` 或访问 http://localhost:8765/stocks

---

## 📊 API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/chat` | POST | 聊天查询 |
| `/tools` | GET | 工具列表 |
| `/stocks` | GET | 股票列表 |

**完整API文档**: http://localhost:8765/docs

---

## ❓ 常见问题

<details>
<summary><b>Q1: 需要GPU吗？</b></summary>

**A**: 不需要。默认使用Mock模式，无需GPU即可运行。如需真实LLM，推荐RTX 3060 6GB以上。
</details>

<details>
<summary><b>Q2: 如何切换到真实模型？</b></summary>

**A**: 
1. 下载模型：`python scripts/download_model.py --model chatglm3-6b-int4`
2. 修改配置：编辑 `server/configs/server_config.yaml`，设置 `mock_mode: false`
3. 重启服务：`python start_server.py`
</details>

<details>
<summary><b>Q3: 数据多久更新？</b></summary>

**A**: 当前是静态数据。可定时运行 `python scripts/download_stock_data.py` 更新。
</details>

<details>
<summary><b>Q4: 如何添加更多股票？</b></summary>

**A**: 编辑 `scripts/download_stock_data.py`，在 `STOCK_LIST` 中添加股票代码和名称，然后重新运行脚本。
</details>

<details>
<summary><b>Q5: 局域网如何访问？</b></summary>

**A**: 
- 服务器：`python start_server.py`（默认监听0.0.0.0）
- 客户端：`python start_client.py http://服务器IP:8765`
</details>

---

## 🚦 故障排查

### 问题1: 端口被占用

**错误**: `Address already in use: 8765`

**解决**: 修改 `server/configs/server_config.yaml` 中的 `port` 为其他值（如8888）

### 问题2: 模块未找到

**错误**: `ModuleNotFoundError: No module named 'xxx'`

**解决**: 
```bash
pip install -r requirements.txt
pip install -r server/requirements.txt
pip install -r client/requirements.txt
```

### 问题3: 数据文件不存在

**错误**: `FileNotFoundError: data/stocks/xxx.parquet`

**解决**: 运行 `python scripts/download_stock_data.py` 下载数据

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可

MIT License

**免责声明**: 投资有风险，入市需谨慎。本系统仅供学习研究使用，不构成任何投资建议。

---

## 🎉 致谢

- [ChatGLM3-6B](https://github.com/THUDM/ChatGLM3) - 清华KEG实验室
- [LangChain](https://github.com/langchain-ai/langchain) - Agent框架
- [akshare](https://github.com/akfamily/akshare) - 金融数据接口
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架

---

**开始使用** → 按照上面的【快速开始】步骤操作即可！

有问题？查看 [QUICKSTART.md](./QUICKSTART.md) 或 [USAGE_GUIDE.md](./USAGE_GUIDE.md)
