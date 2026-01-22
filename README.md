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
- 🐳 **Docker部署**：一键启动，**容器内自动下载模型**
- 🌐 **API接口**：FastAPI RESTful服务

---

## 🚀 使用方式

选择一种方式开始：

- **[方式1：Docker部署](#方式1docker部署)** - **推荐！容器内自动下载模型，无需配置宿主机环境**
- **[方式2：本地使用](#方式2本地使用)** - 直接运行Python代码（开发/调试）

---

## 方式1：Docker部署（推荐）

> **零配置！** 自动使用镜像加速，国内外都能用，开箱即用！

### Mock模式（无需GPU，快速体验）

**仅需两步**：

```bash
# 1. 克隆代码
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent

# 2. 一键启动（自动处理一切）
docker-compose --profile mock up -d
```

**就这么简单！** 容器会自动：
- ✅ 构建Docker镜像
- ✅ 安装所有依赖
- ✅ 启动服务（Mock模式无需下载模型）

#### 步骤3：查看日志

```bash
docker-compose logs -f agent-mock
```

应该看到：
```
==========================================
股票咨询Agent - Docker启动
==========================================
ℹ️  跳过模型自动下载（AUTO_DOWNLOAD_MODEL=false）

==========================================
🚀 启动Agent服务...
==========================================

INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8765
```

#### 步骤4：使用服务

**浏览器测试**（推荐）：

访问 http://localhost:8765/docs

点击 `POST /chat` → `Try it out` → 输入：
```json
{"query": "比亚迪现在多少钱？"}
```

**命令行测试**：
```bash
curl -X POST http://localhost:8765/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "比亚迪现在多少钱？"}'
```

**Python调用**：
```python
import requests

response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "比亚迪现在多少钱？"}
)
print(response.json()['answer'])
```

#### 停止服务

```bash
docker-compose --profile mock down
```

---

### GPU模式（需要NVIDIA GPU）

> **零配置！** 模型自动下载，镜像自动加速，完全容器化！

**仅需三步**：

```bash
# 1. 克隆代码
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent

# 2. 修改配置（改一行）
# 编辑 server/configs/server_config.yaml
# 将 mock_mode: true 改为 mock_mode: false

# 3. 一键启动（自动下载模型 + 自动镜像加速）
docker-compose --profile chatglm3 up -d
```

**容器会自动完成**：
- ✅ 构建Docker镜像（包含CUDA环境）
- ✅ 安装所有Python依赖（含huggingface_hub）
- ✅ **检测模型是否存在**
- ✅ **自动下载ChatGLM3-6B模型**（约4GB，15-30分钟）
- ✅ 启动GPU服务

**完全不依赖宿主机的pip环境！**

#### 步骤4：查看下载进度

```bash
docker-compose logs -f agent-chatglm3
```

你会看到：
```
==========================================
股票咨询Agent - Docker启动
==========================================

📥 检查模型文件...
⚠️  模型不存在，开始自动下载...

模型: chatglm3-6b-int4
目标路径: /app/models/chatglm3-6b

[1/5] 检查依赖...
[2/5] 检查磁盘空间...
[3/5] 检查目标路径...
[4/5] 配置下载参数...
[5/5] 开始下载模型...

下载进度: 45%...
...
✅ 模型下载完成！

==========================================
🚀 启动Agent服务...
==========================================

正在加载模型: ./models/chatglm3-6b
Agent初始化完成：LLM=ChatGLM3LLM, 工具数=5
INFO:     Uvicorn running on http://0.0.0.0:8765
```

#### 步骤5：使用服务

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

#### 停止服务

```bash
docker-compose --profile chatglm3 down
```

#### 自动化设计

✅ **Docker镜像加速**：自动使用南京大学镜像，国内外都可用  
✅ **模型自动下载**：容器启动时自动检测并下载模型  
✅ **HuggingFace镜像**：自动配置国内镜像站  

**无需任何手动配置，开箱即用！**

---

### 高级配置（可选）

#### 使用已有模型

如果你已有模型文件，将其放到 `./models/chatglm3-6b/`，容器会自动检测并跳过下载。

#### 更换镜像源

如需使用官方Docker源（国外或有代理），创建 `.env` 文件：

```bash
REGISTRY_MIRROR=
```

详见 [NETWORK_GUIDE.md](./NETWORK_GUIDE.md)

---

## 方式2：本地使用

> **适合开发调试**，但需要配置Python环境

### 步骤1：克隆代码

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

### 步骤4：启动服务（Mock模式）

```bash
python start_server.py
```

服务启动后：
```
============================================================
股票咨询Agent服务器
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8765
```

### 步骤5：使用服务

**命令行客户端**（新开终端）：
```bash
cd stock-agent
python start_client.py

# 开始对话
您: 比亚迪现在多少钱？
Agent: 【比亚迪(002594)】最新行情：收盘价94.10元...

您: exit  # 退出
```

**API调用**：
```python
import requests

response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "比亚迪现在多少钱？"}
)
print(response.json()['answer'])
```

**浏览器测试**：

访问 http://localhost:8765/docs

---

### GPU模式（本地）

如果有GPU且想在本地运行真实LLM：

```bash
# 1. 安装下载工具
pip install huggingface_hub

# 2. 下载模型
python scripts/download_model.py --model chatglm3-6b-int4

# 3. 修改配置
# 编辑 server/configs/server_config.yaml
# 改为: mock_mode: false

# 4. 重启服务
python start_server.py
```

**详细指南**: [LOCAL_GPU_GUIDE.md](./LOCAL_GPU_GUIDE.md)

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
- 部署: Docker + Docker Compose

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

**Docker环境变量**（`docker-compose.yml`）：

```yaml
environment:
  - AUTO_DOWNLOAD_MODEL=true              # 自动下载模型
  - MODEL_NAME=chatglm3-6b-int4           # 模型名称
  - MODEL_PATH=/app/models/chatglm3-6b    # 模型路径
  - HF_ENDPOINT=https://hf-mirror.com     # 镜像站
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
- 浏览器：http://localhost:8765/stocks
- CLI：输入 `/stocks`

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
<summary><b>Q1: Docker模式需要配置什么吗？</b></summary>

**A**: **不需要任何配置！** 开箱即用：
- ✅ Docker镜像自动加速（默认使用南京大学镜像）
- ✅ 模型自动下载（容器内完成）
- ✅ HuggingFace自动镜像（国内加速）

只需要：
```bash
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent
docker-compose --profile chatglm3 up -d
```
</details>

<details>
<summary><b>Q2: 国外用户会受镜像影响吗？</b></summary>

**A**: 不会。南京大学镜像国内外都可用，速度稳定。

如需使用官方源，创建 `.env`：
```bash
REGISTRY_MIRROR=
```
</details>

<details>
<summary><b>Q3: 网络问题怎么办？</b></summary>

**A**: 
1. **Docker镜像拉取失败**：已自动使用镜像加速，通常不会失败
2. **模型下载失败**：已自动配置HuggingFace镜像站
3. **仍有问题**：查看 [NETWORK_GUIDE.md](./NETWORK_GUIDE.md)
</details>

<details>
<summary><b>Q4: Mock模式和GPU模式有什么区别？</b></summary>

**A**:
- **Mock模式**: 使用预设模板回答，速度快，无需GPU，适合开发测试
- **GPU模式**: 使用真实LLM（ChatGLM3），回答质量高，需要显卡
</details>

<details>
<summary><b>Q5: 需要什么GPU？</b></summary>

**A**:
- **ChatGLM3-6B INT4**: RTX 3060 6GB+ / RTX 3070 8GB / RTX 4060
- **Qwen2-7B INT4**: RTX 3080 10GB+ / RTX 4070
- **无GPU**: 使用Mock模式
</details>

<details>
<summary><b>Q6: 如何添加更多股票？</b></summary>

**A**: 编辑 `scripts/download_stock_data.py`，在 `STOCK_LIST` 中添加股票：
```python
STOCK_LIST = [
    ("比亚迪", "002594"),
    ("你的股票", "代码"),
    # ...
]
```

重新运行：
```bash
python scripts/download_stock_data.py  # 本地模式
# 或
docker-compose restart agent-xxx       # Docker模式
```
</details>

<details>
<summary><b>Q7: 局域网如何访问？</b></summary>

**A**:
- 服务器默认监听 `0.0.0.0`，局域网内可访问
- 客户端连接: `python start_client.py http://服务器IP:8765`
- 浏览器访问: `http://服务器IP:8765/docs`
</details>

<details>
<summary><b>Q8: 如何更新到最新版本？</b></summary>

**A**:
```bash
cd stock-agent
git pull origin main
docker-compose --profile chatglm3 down
docker-compose --profile chatglm3 up -d --build
```
</details>

---

## 🚦 故障排查

### 问题1: Docker构建失败

**错误**: `Cannot connect to the Docker daemon`

**解决**:
```bash
# 启动Docker服务
sudo systemctl start docker  # Linux
# 或打开Docker Desktop      # Windows/Mac
```

### 问题2: GPU不可用

**错误**: `could not select device driver "" with capabilities: [[gpu]]`

**解决**:
1. 安装NVIDIA Docker Runtime:
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

2. 验证:
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### 问题3: 端口被占用

**错误**: `Bind for 0.0.0.0:8765 failed: port is already allocated`

**解决**: 修改 `docker-compose.yml`：
```yaml
ports:
  - "8766:8765"  # 改为其他端口
```

### 问题4: 模型下载失败

**错误**: `Failed to download model`

**解决**:
1. 检查磁盘空间（需要>10GB）
2. 检查网络连接（需访问huggingface.co或镜像站）
3. 或手动下载后挂载：
```bash
# 将模型放到 ./models/chatglm3-6b/
# 修改 docker-compose.yml: AUTO_DOWNLOAD_MODEL=false
```

### 问题5: 容器启动后立即退出

**检查日志**:
```bash
docker-compose logs agent-chatglm3
```

常见原因：
- 配置文件错误（`server_config.yaml`）
- 模型路径不正确
- GPU驱动未安装

---

## 📚 完整文档

| 文档 | 说明 |
|------|------|
| [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) | Docker详细文档 |
| [LOCAL_GPU_GUIDE.md](./LOCAL_GPU_GUIDE.md) | 本地GPU部署指南 |
| [MODEL_GUIDE.md](./MODEL_GUIDE.md) | 模型选择指南 |
| [TOOLS_GUIDE.md](./TOOLS_GUIDE.md) | 工具使用说明 |
| [USAGE_GUIDE.md](./USAGE_GUIDE.md) | 完整使用手册 |

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

- 🐳 **推荐：[Docker部署](#方式1docker部署)** - 零配置，容器内自动下载模型
- 📖 [本地使用](#方式2本地使用) - 开发调试模式
