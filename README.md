# 股票咨询Agent系统 🚀

基于LangGraph和ChatGLM的智能股票分析AI Agent，支持实时数据查询、技术指标分析、知识问答。

[![GitHub](https://img.shields.io/badge/GitHub-conan7072%2Fstock--agent-blue)](https://github.com/conan7072/stock-agent)
[![Docker](https://img.shields.io/badge/Docker-支持-2496ED?logo=docker)](https://github.com/conan7072/stock-agent)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)

---

## ✨ 特性

- 📈 **真实数据**：50只A股热门股票，6年历史数据
- 🤖 **智能对话**：基于LLM的自然语言交互
- 🔧 **5大工具**：价格查询、技术指标、历史数据、股票对比、综合分析
- 📚 **知识库**：金融术语RAG检索
- 🐳 **Docker部署**：一键启动
- 🌐 **API接口**：FastAPI RESTful服务

---

## 🚀 使用方式

选择一种方式开始：

- **[方式1：本地使用](#方式1本地使用)** - 直接运行Python代码（开发/测试）
- **[方式2：Docker部署](#方式2docker部署)** - 容器化部署（生产推荐）

---

## 方式1：本地使用

### 步骤1：克隆代码

```bash
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent
```

### 步骤2：安装依赖

```bash
# 安装所有依赖
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

### 步骤4：启动服务（Mock模式，无需GPU）

```bash
# 启动服务端
python start_server.py
```

服务启动后会显示：
```
============================================================
股票咨询Agent服务器
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8765
```

### 步骤5：使用服务

#### 方式A：命令行客户端

新开一个终端：
```bash
cd stock-agent
python start_client.py

# 开始对话
您: 比亚迪现在多少钱？
Agent: 【比亚迪(002594)】最新行情：收盘价94.10元...

您: 什么是MACD指标？
Agent: MACD是异同移动平均线...

您: exit  # 退出
```

#### 方式B：API调用

```python
import requests

response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "比亚迪现在多少钱？"}
)
print(response.json()['answer'])
```

#### 方式C：浏览器测试

访问 http://localhost:8765/docs

在Swagger UI中：
1. 点击 `POST /chat`
2. 点击 "Try it out"
3. 输入：`{"query": "比亚迪现在多少钱？"}`
4. 点击 "Execute"

### GPU模式（可选，需要显卡）

如果有GPU（如RTX 3070），可以使用真实LLM：

```bash
# 1. 安装下载工具
pip install huggingface_hub

# 2. 下载模型（约15-30分钟）
python scripts/download_model.py --model chatglm3-6b-int4

# 3. 修改配置
# 编辑 server/configs/server_config.yaml
# 改为: mock_mode: false

# 4. 重启服务
python start_server.py
```

**详细GPU部署指南**: [LOCAL_GPU_GUIDE.md](./LOCAL_GPU_GUIDE.md)

---

## 方式2：Docker部署

### Mock模式（无需GPU，推荐测试）

#### 步骤1：克隆代码

```bash
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent
```

#### 步骤2：启动服务

```bash
docker-compose --profile mock up -d
```

#### 步骤3：查看日志

```bash
docker-compose logs -f agent-mock
```

应该看到：
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8765
```

#### 步骤4：使用服务

**浏览器测试**：
访问 http://localhost:8765/docs

**API调用**：
```python
import requests

response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "比亚迪现在多少钱？"}
)
print(response.json()['answer'])
```

**命令行**：
```bash
curl -X POST http://localhost:8765/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "比亚迪现在多少钱？"}'
```

#### 停止服务

```bash
docker-compose --profile mock down
```

---

### GPU模式（需要NVIDIA GPU）

#### 步骤1：克隆代码

```bash
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent
```

#### 步骤2：下载模型

```bash
# 安装下载工具
pip install huggingface_hub

# 下载模型（约15-30分钟）
python scripts/download_model.py --model chatglm3-6b-int4
```

模型会下载到 `./models/chatglm3-6b`

#### 步骤3：修改配置

编辑 `server/configs/server_config.yaml`：

```yaml
model:
  mock_mode: false              # 改为 false
  name: chatglm3-6b
  path: ./models/chatglm3-6b
  device: cuda
  quantization: int4

server:
  host: 0.0.0.0
  port: 8765
```

#### 步骤4：启动服务

```bash
docker-compose --profile chatglm3 up -d
```

#### 步骤5：查看日志

```bash
docker-compose logs -f agent-chatglm3
```

应该看到：
```
正在加载模型: ./models/chatglm3-6b
Agent初始化完成：LLM=ChatGLM3LLM, 工具数=5
INFO:     Uvicorn running on http://0.0.0.0:8765
```

#### 步骤6：使用服务

**浏览器测试**：
访问 http://localhost:8765/docs

**API调用**：
```python
import requests

response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "分析一下贵州茅台"}
)
print(response.json()['answer'])
```

**命令行**：
```bash
curl -X POST http://localhost:8765/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "分析一下贵州茅台"}'
```

#### 停止服务

```bash
docker-compose --profile chatglm3 down
```

**完整GPU部署指南**: [LOCAL_GPU_GUIDE.md](./LOCAL_GPU_GUIDE.md)

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

## 📚 完整文档

| 文档 | 说明 |
|------|------|
| [LOCAL_GPU_GUIDE.md](./LOCAL_GPU_GUIDE.md) | GPU部署完整指南 |
| [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) | Docker详细文档 |
| [MODEL_GUIDE.md](./MODEL_GUIDE.md) | 模型选择指南 |
| [TOOLS_GUIDE.md](./TOOLS_GUIDE.md) | 工具使用说明 |
| [USAGE_GUIDE.md](./USAGE_GUIDE.md) | 完整使用手册 |
| [QUICKSTART.md](./QUICKSTART.md) | 快速开始指南 |

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

## ⚙️ 配置说明

编辑 `server/configs/server_config.yaml`：

```yaml
# 模型配置
model:
  mock_mode: true          # true=Mock模式, false=真实LLM
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

**查看完整列表**: 
- 运行客户端后输入 `/stocks`
- 访问 http://localhost:8765/stocks

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

**A**: 不需要。默认使用Mock模式，无需GPU。如需真实LLM，推荐RTX 3060 6GB以上。
</details>

<details>
<summary><b>Q2: Mock模式和GPU模式有什么区别？</b></summary>

**A**: 
- **Mock模式**: 使用预设模板回答，速度快，无需GPU，适合开发测试
- **GPU模式**: 使用真实LLM（ChatGLM3），回答质量高，需要显卡
</details>

<details>
<summary><b>Q3: 如何添加更多股票？</b></summary>

**A**: 编辑 `scripts/download_stock_data.py`，在 `STOCK_LIST` 中添加股票代码和名称，然后重新运行：
```bash
python scripts/download_stock_data.py
```
</details>

<details>
<summary><b>Q4: 数据多久更新？</b></summary>

**A**: 当前是静态数据。可定时运行更新：
```bash
python scripts/download_stock_data.py
```
</details>

<details>
<summary><b>Q5: 局域网如何访问？</b></summary>

**A**: 
- 服务器默认监听 `0.0.0.0`，局域网内可访问
- 客户端连接: `python start_client.py http://服务器IP:8765`
</details>

<details>
<summary><b>Q6: Docker找不到模型？</b></summary>

**A**: 确保：
1. 模型已下载到 `./models/chatglm3-6b`
2. 配置文件中 `mock_mode: false`
3. 使用正确的profile: `docker-compose --profile chatglm3 up -d`
</details>

---

## 🚦 故障排查

### 问题1: 端口被占用

**错误**: `Address already in use: 8765`

**解决**: 修改 `server/configs/server_config.yaml` 中的 `port`

### 问题2: 模块未找到

**错误**: `ModuleNotFoundError: No module named 'xxx'`

**解决**: 
```bash
pip install -r requirements.txt
pip install -r server/requirements.txt
pip install -r client/requirements.txt
```

### 问题3: 下载模型无反应

**原因**: 缺少 `huggingface_hub`

**解决**: 
```bash
pip install huggingface_hub
```

### 问题4: GPU未被使用

**检查**:
1. 安装NVIDIA Docker: `docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi`
2. 配置文件: `device: cuda`
3. Docker配置: 使用 `--profile chatglm3`

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

**选择你的使用方式开始吧！** 🚀

- 📖 [本地使用](#方式1本地使用)
- 🐳 [Docker部署](#方式2docker部署)
