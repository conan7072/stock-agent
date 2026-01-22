# 本地GPU部署完整指南

**适用场景**: 在有GPU的机器（如RTX 3070）上部署真实LLM

---

## ✅ 你的流程是对的！

**步骤**: git clone → 下载模型 → docker部署

**路径确认**: 
- ✅ 模型下载路径: `./models/chatglm3-6b` (相对路径)
- ✅ Docker自动挂载: `./models` → `/app/models` (容器内)
- ✅ 配置文件路径: `./models/chatglm3-6b` (相对于项目根目录)

---

## 📋 完整部署步骤（3070机器）

### 步骤1：获取代码

```bash
# 如果是第一次
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent

# 如果已经clone过，更新到最新版
cd stock-agent
git pull origin main
```

**验证**:
```bash
ls -la
# 应该看到：server/ client/ scripts/ data/ Dockerfile docker-compose.yml 等
```

---

### 步骤2：安装下载依赖

```bash
# 安装huggingface_hub（下载模型必需）
pip install huggingface_hub

# 或安装完整依赖
pip install -r requirements.txt
```

### 步骤3：下载模型

```bash
# 下载ChatGLM3-6B INT4（适合RTX 3070 8GB）
python scripts/download_model.py --model chatglm3-6b-int4
```

**预期输出**:
```
======================================================================
模型下载工具 - chatglm3-6b-int4
======================================================================

模型: chatglm3-6b-int4
描述: ChatGLM3-6B INT4量化版（推荐RTX 3070）
文件大小: ~13GB
显存需求: 4-5GB
保存路径: ./models/chatglm3-6b
Hugging Face: THUDM/chatglm3-6b

[步骤 1/5] 检查依赖...
✓ huggingface_hub 已安装

[步骤 2/5] 检查磁盘空间...
当前目录可用空间: 125.3 GB
✓ 磁盘空间充足

[步骤 3/5] 检查现有文件...
✓ 目录为空，准备下载

[步骤 4/5] 配置下载...
✓ 使用镜像: https://hf-mirror.com

[步骤 5/5] 开始下载...
正在从 Hugging Face 下载...
仓库: THUDM/chatglm3-6b

... (下载过程，可能需要10-30分钟)

======================================================================
✓ 下载完成！
======================================================================

耗时: 15.3 分钟
路径: ./models/chatglm3-6b
```

**验证**:
```bash
ls -la models/chatglm3-6b/
# 应该看到模型文件（config.json, pytorch_model.bin等）
```

---

### 步骤4：修改配置

编辑 `server/configs/server_config.yaml`：

```yaml
model:
  mock_mode: false              # ← 改为 false（重要！）
  name: chatglm3-6b
  path: ./models/chatglm3-6b    # ← 相对路径，Docker会自动挂载
  device: cuda                  # ← 使用GPU
  quantization: int4
  max_length: 4096
  temperature: 0.7
  top_p: 0.9

server:
  host: 0.0.0.0
  port: 8765
```

**验证**:
```bash
cat server/configs/server_config.yaml | grep mock_mode
# 应该显示: mock_mode: false
```

---

### 步骤5：Docker部署

```bash
# 启动GPU版本（ChatGLM3）
docker-compose --profile chatglm3 up -d
```

**预期输出**:
```
[+] Running 1/1
 ✔ Container stock-agent-chatglm3  Started
```

**查看日志**:
```bash
docker-compose logs -f agent-chatglm3
```

**预期日志**:
```
============================================================
🚀 启动股票咨询Agent服务...
============================================================
模式: gpu
端口: 8765
时间: Thu Jan 22 12:34:56 UTC 2026
============================================================

INFO:     Started server process [1]
INFO:     Waiting for application startup.
============================================================
启动股票咨询Agent服务...
============================================================
正在加载模型: ./models/chatglm3-6b
已加载 21 条知识库索引
Agent初始化完成：LLM=ChatGLM3LLM, 工具数=5

服务已启动:
  - Host: 0.0.0.0
  - Port: 8765
  - API Docs: http://0.0.0.0:8765/docs
============================================================
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8765 (Press CTRL+C to quit)
```

---

### 步骤6：测试服务

**测试健康检查**:
```bash
curl http://localhost:8765/health
```

**预期输出**:
```json
{
  "status": "healthy",
  "agent_ready": true
}
```

**测试聊天**:
```bash
curl -X POST http://localhost:8765/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "比亚迪现在多少钱？"}'
```

**或使用浏览器**:
访问 http://localhost:8765/docs 进行交互式测试

---

## 📂 路径说明

### 项目结构
```
stock-agent/                    (项目根目录)
├── models/                     ← 模型存放（你下载的）
│   └── chatglm3-6b/           
│       ├── config.json
│       ├── pytorch_model.bin
│       └── tokenizer_config.json
├── data/                       ← 数据文件
│   ├── stocks/                
│   └── knowledge/
├── server/
│   ├── configs/
│   │   └── server_config.yaml  ← 配置文件
│   └── src/
├── Dockerfile
└── docker-compose.yml
```

### Docker挂载配置

在 `docker-compose.yml` 中（GPU版本）：

```yaml
volumes:
  - ./data:/app/data              # 数据目录
  - ./models:/app/models          # ← 模型目录（挂载到容器）
  - ./server/configs:/app/server/configs  # 配置目录
  - ./logs:/app/logs              # 日志目录
```

**工作原理**:
1. 你在主机下载模型到: `./models/chatglm3-6b`
2. Docker启动时自动挂载: `./models` → `/app/models`
3. 容器内访问路径: `/app/models/chatglm3-6b`
4. 配置文件中使用相对路径: `./models/chatglm3-6b`
5. 容器内自动解析为: `/app/models/chatglm3-6b` ✓

**所以你的流程完全正确！** ✅

---

## 🔍 验证路径是否正确

### 方法1：检查配置
```bash
# 主机上
cat server/configs/server_config.yaml | grep path
# 输出: path: ./models/chatglm3-6b
```

### 方法2：进入容器检查
```bash
# 进入运行中的容器
docker exec -it stock-agent-chatglm3 bash

# 检查模型文件是否存在
ls -la /app/models/chatglm3-6b/

# 应该看到模型文件
# config.json
# pytorch_model.bin
# ...

# 退出容器
exit
```

### 方法3：查看日志
```bash
docker-compose logs agent-chatglm3 | grep "模型"

# 应该看到类似：
# 正在加载模型: ./models/chatglm3-6b
# 模型加载成功
```

---

## ⚠️ 常见问题

### Q1: 模型下载失败

**错误**: `网络连接超时` 或 `下载中断`

**解决**:
```bash
# 下载脚本支持断点续传，直接重新运行即可
python scripts/download_model.py --model chatglm3-6b-int4
```

### Q2: Docker找不到模型

**错误**: 容器日志显示 `FileNotFoundError: models/chatglm3-6b`

**检查**:
```bash
# 1. 确认模型已下载
ls -la models/chatglm3-6b/

# 2. 确认docker-compose.yml有volumes配置
grep -A2 "volumes:" docker-compose.yml

# 3. 确认使用了正确的profile
docker-compose --profile chatglm3 up -d  # ← 必须指定profile
```

### Q3: GPU未被使用

**错误**: 容器日志显示使用CPU

**检查**:
```bash
# 1. 确认NVIDIA Docker已安装
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# 2. 确认配置文件中 device: cuda
cat server/configs/server_config.yaml | grep device

# 3. 确认docker-compose.yml有GPU配置
grep -A5 "deploy:" docker-compose.yml
```

### Q4: 磁盘空间不足

**错误**: 下载中途失败，提示空间不足

**解决**:
```bash
# 清理Docker镜像释放空间
docker system prune -a

# 或使用更大的磁盘
# 修改 download_model.py 中的 model_info['path'] 为其他路径
```

---

## 🎯 快速命令参考

```bash
# 1. 克隆/更新代码
git clone https://github.com/conan7072/stock-agent.git
cd stock-agent
# 或
git pull origin main

# 2. 下载模型
python scripts/download_model.py --model chatglm3-6b-int4

# 3. 修改配置
vim server/configs/server_config.yaml
# 设置 mock_mode: false

# 4. 启动服务
docker-compose --profile chatglm3 up -d

# 5. 查看日志
docker-compose logs -f agent-chatglm3

# 6. 测试服务
curl http://localhost:8765/health

# 7. 停止服务
docker-compose --profile chatglm3 down
```

---

## 📊 性能预期（RTX 3070 8GB）

| 指标 | 值 |
|------|-----|
| **显存占用** | 4-5GB |
| **首次响应** | 1-2秒 |
| **生成速度** | 15-20 tokens/s |
| **并发支持** | 2-3人 |
| **推理质量** | 优秀 |

---

## ✅ 总结

**你的流程完全正确**：

1. ✅ `git clone` 获取代码
2. ✅ `python scripts/download_model.py` 下载模型到 `./models/`
3. ✅ 修改配置 `mock_mode: false`
4. ✅ `docker-compose --profile chatglm3 up -d` 启动
5. ✅ Docker自动挂载 `./models` → `/app/models`
6. ✅ 容器内正确读取模型 ✓

**路径是相对路径，Docker能读到！** ✅

---

**开始在你的3070机器上部署吧！** 🚀
