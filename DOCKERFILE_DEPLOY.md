# Dockerfile部署方案对比

本项目提供**两种Dockerfile**，适用于不同场景：

---

## 📋 方案对比

| 特性 | Dockerfile（本地构建） | Dockerfile.standalone（自包含） |
|------|---------------------|--------------------------|
| **依赖** | 需要完整项目文件 | 只需要Dockerfile |
| **构建源** | 本地文件 | Git仓库 |
| **适用场景** | 本地开发、CI/CD | 快速分发、远程部署 |
| **优点** | 构建快速、可调试 | 随处可构建 |
| **缺点** | 需要传输整个项目 | 需要Git仓库 |
| **推荐用途** | 开发测试 | 生产部署 |

---

## 🎯 场景1：本地开发（使用Dockerfile）

### 适用情况
- ✅ 在开发机器上构建
- ✅ 有完整项目文件
- ✅ 需要频繁修改代码
- ✅ CI/CD流程中

### 使用方法

```bash
# 确保在项目根目录
cd c:\project\agent

# 构建Mock模式
docker build --build-arg MODE=mock -t stock-agent:mock .

# 构建GPU模式
docker build --build-arg MODE=gpu -t stock-agent:chatglm3 .
```

### 依赖文件
```
项目根目录/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── server/
├── client/
├── scripts/
├── data/
├── start_server.py
└── start_client.py
```

---

## 🚀 场景2：远程部署（使用Dockerfile.standalone）

### 适用情况
- ✅ 代码已推送到Git仓库
- ✅ 在新机器上快速部署
- ✅ 分享给其他人使用
- ✅ 云服务器部署

### 前提条件

**1. 将项目推送到Git仓库**

```bash
# 如果还没有Git仓库，初始化
cd c:\project\agent
git init

# 添加所有文件
git add .
git commit -m "Initial commit"

# 推送到远程仓库（GitHub/GitLab/Gitee）
git remote add origin https://github.com/yourname/stock-agent.git
git push -u origin main
```

### 使用方法

**在任何机器上**，只需要 `Dockerfile.standalone` 文件：

```bash
# 创建一个空目录
mkdir stock-agent-deploy
cd stock-agent-deploy

# 下载Dockerfile.standalone（或从本文档复制）
curl -O https://raw.githubusercontent.com/yourname/stock-agent/main/Dockerfile.standalone

# 构建（替换为你的Git仓库地址）
docker build -f Dockerfile.standalone \
  --build-arg MODE=mock \
  --build-arg GIT_REPO=https://github.com/yourname/stock-agent.git \
  --build-arg GIT_BRANCH=main \
  -t stock-agent:mock .

# 启动
docker run -d -p 8765:8765 --name stock-agent stock-agent:mock
```

### 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `MODE` | 构建模式 | `mock` | `mock`, `gpu` |
| `GIT_REPO` | Git仓库地址 | 必填 | `https://github.com/user/repo.git` |
| `GIT_BRANCH` | Git分支 | `main` | `main`, `develop` |

---

## 🌐 场景3：公开分享（使用Docker Hub）

### 步骤1：构建并推送镜像

```bash
# 本地构建
docker build --build-arg MODE=mock -t yourname/stock-agent:mock .
docker build --build-arg MODE=gpu -t yourname/stock-agent:chatglm3 .

# 登录Docker Hub
docker login

# 推送镜像
docker push yourname/stock-agent:mock
docker push yourname/stock-agent:chatglm3
```

### 步骤2：其他人使用

```bash
# 直接拉取运行，无需任何文件
docker run -d -p 8765:8765 yourname/stock-agent:mock
```

---

## 📊 详细对比

### 方案1：Dockerfile（当前使用）

**优点**：
- ✅ 构建速度快（无需从网络下载）
- ✅ 支持本地修改和调试
- ✅ 不依赖网络连接
- ✅ 适合CI/CD流水线

**缺点**：
- ❌ 需要传输整个项目（可能几百MB）
- ❌ 依赖多个文件和目录
- ❌ 不便于快速分享

**适用场景**：
- 开发环境
- 测试环境
- CI/CD构建
- 有完整项目代码的情况

---

### 方案2：Dockerfile.standalone（新增）

**优点**：
- ✅ 只需一个文件即可构建
- ✅ 便于分享和分发
- ✅ 代码版本化管理
- ✅ 自动获取最新代码

**缺点**：
- ❌ 需要Git仓库
- ❌ 依赖网络连接
- ❌ 构建时间稍长（需要克隆）
- ❌ 不适合频繁修改

**适用场景**：
- 生产环境部署
- 云服务器部署
- 分享给其他开发者
- 快速体验项目

---

## 🎓 使用示例

### 示例1：本地开发（Dockerfile）

```bash
# 场景：在开发机上频繁修改代码并测试

# 修改代码
vim server/src/agent/stock_agent.py

# 重新构建
docker build -t stock-agent:mock .

# 测试
docker run -d -p 8765:8765 stock-agent:mock
```

**优势**：快速迭代

---

### 示例2：部署到新服务器（Dockerfile.standalone）

```bash
# 场景：在新的云服务器上部署

# 只需要一个命令（假设Dockerfile.standalone已上传）
docker build -f Dockerfile.standalone \
  --build-arg GIT_REPO=https://github.com/yourname/stock-agent.git \
  -t stock-agent:mock . && \
docker run -d -p 8765:8765 stock-agent:mock
```

**优势**：无需传输项目文件

---

### 示例3：分享给同事（Docker Hub）

```bash
# 你的操作
docker build -t yourname/stock-agent:mock .
docker push yourname/stock-agent:mock

# 同事的操作（只需一行）
docker run -d -p 8765:8765 yourname/stock-agent:mock
```

**优势**：极简体验

---

## 🔧 Git仓库配置

### 如果使用Dockerfile.standalone，需要先配置Git仓库：

#### 选项1：GitHub

```bash
# 1. 在GitHub创建仓库
# 访问 https://github.com/new

# 2. 推送代码
cd c:\project\agent
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourname/stock-agent.git
git push -u origin main
```

#### 选项2：Gitee（国内）

```bash
# 1. 在Gitee创建仓库
# 访问 https://gitee.com/projects/new

# 2. 推送代码
cd c:\project\agent
git init
git add .
git commit -m "Initial commit"
git remote add origin https://gitee.com/yourname/stock-agent.git
git push -u origin main
```

#### 选项3：私有GitLab

```bash
git remote add origin https://gitlab.yourcompany.com/yourname/stock-agent.git
git push -u origin main
```

---

## 📝 .dockerignore 优化

为了减小构建上下文，添加 `.dockerignore`：

```
# 已在项目中
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.git/
.venv/
venv/
models/
logs/
*.log

# 大文件
data/stocks/*.parquet  # 如果使用standalone，会从Git下载
```

---

## 🎯 推荐策略

### 开发阶段
```bash
# 使用本地Dockerfile
docker build -t stock-agent:dev .
```

### 测试阶段
```bash
# 使用本地Dockerfile + docker-compose
docker-compose --profile mock up -d
```

### 生产部署
```bash
# 方案A: 使用Dockerfile.standalone
docker build -f Dockerfile.standalone \
  --build-arg GIT_REPO=https://github.com/yourname/stock-agent.git \
  -t stock-agent:prod .

# 方案B: 使用预构建镜像（Docker Hub）
docker pull yourname/stock-agent:latest
```

---

## ✅ 总结

| 需求 | 推荐方案 | 命令 |
|------|---------|------|
| **本地开发** | Dockerfile | `docker build -t stock-agent .` |
| **快速测试** | docker-compose | `docker-compose up -d` |
| **新机器部署** | Dockerfile.standalone | 见示例2 |
| **分享给他人** | Docker Hub | `docker push/pull` |
| **CI/CD** | Dockerfile | 在流水线中构建 |

---

## 🔗 下一步

1. **如果需要快速分发**：
   - 将项目推送到Git
   - 使用 `Dockerfile.standalone`

2. **如果需要公开分享**：
   - 构建并推送到Docker Hub
   - 提供 `docker run` 命令

3. **如果只是本地开发**：
   - 继续使用当前的 `Dockerfile`
   - 使用 `docker-compose` 管理服务

---

**当前状态**：
- ✅ `Dockerfile` - 已测试，正在使用
- ✅ `Dockerfile.standalone` - 已创建，待推送Git后测试
- ✅ `docker-compose.yml` - 已配置

**你的选择**：根据具体需求选择合适的方案！
