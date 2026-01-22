# Docker部署指南

## 📦 Docker镜像说明

本项目提供统一的Dockerfile，支持多种模式：

1. **stock-agent:mock** - Mock模式（无需GPU，推荐测试）
2. **stock-agent:chatglm3** - ChatGLM3-6B模式（需要GPU）
3. **stock-agent:qwen2** - Qwen2-1.5B模式（需要GPU）

---

## 🚀 快速开始（推荐）

### Windows用户

```bash
# 构建镜像（交互式）
docker_build.bat

# 启动并测试
docker_test.bat
```

### Linux/Mac用户

```bash
# 添加执行权限
chmod +x docker_build.sh docker_test.sh

# 构建镜像（交互式）
./docker_build.sh

# 启动并测试
./docker_test.sh
```

---

## 📋 详细步骤

### 方式1：使用Mock模式（最简单，推荐）

```bash
# 1. 构建镜像
docker build --build-arg MODE=mock -t stock-agent:mock .

# 2. 启动服务
docker-compose --profile mock up -d

# 3. 查看日志
docker-compose logs -f agent-mock

# 4. 测试
curl http://localhost:8765/health
```

### 方式2：使用GPU版本

**前提条件**：
- 安装NVIDIA Docker：https://github.com/NVIDIA/nvidia-docker
- 有可用的NVIDIA GPU

```bash
# 构建并启动GPU版本
docker-compose --profile gpu up -d

# 查看日志
docker-compose logs -f agent-gpu

# 测试
curl http://localhost:8765/health
```

### 方式3：完整部署（服务器+客户端）

```bash
# 启动服务器（CPU版本）
docker-compose --profile cpu up -d agent-cpu

# 启动客户端
docker-compose --profile client up agent-client
```

---

## 🔧 手动构建

### 构建CPU版本

```bash
# 构建镜像
docker build -f Dockerfile.cpu -t stock-agent:cpu .

# 运行容器
docker run -d \
  --name stock-agent-cpu \
  -p 8765:8765 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/server/configs:/app/server/configs \
  stock-agent:cpu

# 查看日志
docker logs -f stock-agent-cpu
```

### 构建GPU版本

```bash
# 构建镜像
docker build -f Dockerfile -t stock-agent:gpu .

# 运行容器（需要NVIDIA Docker）
docker run -d \
  --name stock-agent-gpu \
  --gpus all \
  -p 8765:8765 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/server/configs:/app/server/configs \
  stock-agent:gpu

# 查看日志
docker logs -f stock-agent-gpu
```

### 构建客户端

```bash
# 构建镜像
docker build -f Dockerfile.client -t stock-agent:client .

# 运行容器（连接到服务器）
docker run -it \
  --name stock-agent-client \
  -e SERVER_URL=http://host.docker.internal:8765 \
  stock-agent:client
```

---

## 📝 配置说明

### 环境变量

#### 服务器
- `CUDA_VISIBLE_DEVICES`: GPU设备ID（GPU版本）
- `PYTHONUNBUFFERED`: 禁用Python输出缓冲

#### 客户端
- `SERVER_URL`: 服务器地址（默认：http://localhost:8765）

### 挂载卷

#### 服务器
- `./data:/app/data` - 股票数据和知识库
- `./models:/app/models` - 模型文件（GPU版本）
- `./server/configs:/app/server/configs` - 配置文件

---

## 🔍 常用命令

### 查看容器状态

```bash
docker-compose ps
```

### 查看日志

```bash
# 实时日志
docker-compose logs -f agent-cpu

# 最近100行
docker-compose logs --tail=100 agent-cpu
```

### 进入容器

```bash
docker exec -it stock-agent-cpu bash
```

### 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止特定服务
docker-compose stop agent-cpu
```

### 重启服务

```bash
docker-compose restart agent-cpu
```

### 删除容器和镜像

```bash
# 停止并删除容器
docker-compose down

# 删除镜像
docker rmi stock-agent:cpu stock-agent:gpu stock-agent:client
```

---

## 🧪 测试

### 健康检查

```bash
curl http://localhost:8765/health
```

### 聊天测试

```bash
curl -X POST http://localhost:8765/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "比亚迪现在多少钱？"}'
```

### 工具列表

```bash
curl http://localhost:8765/tools
```

### 股票列表

```bash
curl http://localhost:8765/stocks
```

---

## 📊 性能优化

### CPU版本优化

1. **限制资源**：
```bash
docker run -d \
  --name stock-agent-cpu \
  --cpus=2 \
  --memory=4g \
  -p 8765:8765 \
  stock-agent:cpu
```

2. **调整workers数量**：
修改 `server/configs/server_config.yaml`:
```yaml
server:
  workers: 2  # 根据CPU核心数调整
```

### GPU版本优化

1. **指定GPU**：
```bash
docker run -d \
  --gpus '"device=0"' \
  -p 8765:8765 \
  stock-agent:gpu
```

2. **限制显存**：
修改配置文件，减小 `max_length` 或使用更小的模型。

---

## 🌐 多机部署

### 服务器机器

```bash
# 启动服务器
docker-compose --profile cpu up -d

# 开放防火墙（如果需要）
sudo ufw allow 8765
```

### 客户端机器

```bash
# 方式1：使用Docker
docker run -it \
  -e SERVER_URL=http://服务器IP:8765 \
  stock-agent:client

# 方式2：直接使用Python脚本
python start_client.py http://服务器IP:8765
```

---

## 🐛 故障排除

### 问题1：容器无法启动

**检查**：
```bash
docker logs stock-agent-cpu
```

**常见原因**：
- 端口被占用：`lsof -i :8765`
- 数据目录不存在：确保 `./data` 存在

### 问题2：GPU版本无法使用GPU

**检查NVIDIA Docker**：
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base nvidia-smi
```

**安装NVIDIA Docker**：
```bash
# Ubuntu
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 问题3：客户端无法连接服务器

**检查网络**：
```bash
# 在客户端机器上
curl http://服务器IP:8765/health

# 检查防火墙
sudo ufw status
```

---

## 📦 镜像导出和导入

### 导出镜像

```bash
# 保存为tar文件
docker save stock-agent:cpu -o stock-agent-cpu.tar

# 压缩（可选）
gzip stock-agent-cpu.tar
```

### 导入镜像

```bash
# 从tar文件加载
docker load -i stock-agent-cpu.tar

# 或从压缩文件
gunzip -c stock-agent-cpu.tar.gz | docker load
```

### 传输到其他机器

```bash
# 使用scp传输
scp stock-agent-cpu.tar user@remote-host:/path/

# 在远程机器上加载
ssh user@remote-host "docker load -i /path/stock-agent-cpu.tar"
```

---

## 🔄 更新部署

### 重新构建镜像

```bash
# 拉取最新代码
git pull

# 重新构建
docker-compose build agent-cpu

# 重启服务
docker-compose up -d agent-cpu
```

### 不停机更新

```bash
# 启动新容器
docker-compose up -d --scale agent-cpu=2

# 等待新容器就绪（健康检查通过）

# 停止旧容器
docker-compose scale agent-cpu=1
```

---

## 📚 更多资源

- **项目文档**: [README.md](./README.md)
- **使用指南**: [USAGE_GUIDE.md](./USAGE_GUIDE.md)
- **API文档**: http://localhost:8765/docs（启动后访问）

---

## ⚠️ 注意事项

1. **GPU版本需要下载模型**（~13GB），首次启动会较慢
2. **CPU版本使用Mock模式**，响应是预设的模板
3. **生产环境建议**：
   - 使用反向代理（Nginx）
   - 配置SSL证书（HTTPS）
   - 限制访问IP
   - 定期备份数据

---

**开始使用Docker部署吧！** 🚀🐳
