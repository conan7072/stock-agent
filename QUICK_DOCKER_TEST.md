# 🚀 快速Docker测试指南

**5分钟内体验股票咨询Agent！**

---

## 方式1：Windows用户（推荐）

### 步骤1：构建镜像

双击运行或在PowerShell中执行：

```powershell
.\docker_build.bat
```

选择选项 **1** (Mock模式)

### 步骤2：启动并测试

```powershell
.\docker_test.bat
```

选择以下选项进行测试：
- **1**: 启动服务
- **2**: 运行所有测试
- **7**: 交互式测试（与Agent对话）

---

## 方式2：Linux/Mac用户

### 步骤1：添加执行权限

```bash
chmod +x docker_build.sh docker_test.sh
```

### 步骤2：构建镜像

```bash
./docker_build.sh
```

选择选项 **1** (Mock模式)

### 步骤3：启动并测试

```bash
./docker_test.sh
```

---

## 方式3：命令行直接操作

### 一键启动

```bash
# 构建
docker build --build-arg MODE=mock -t stock-agent:mock .

# 启动
docker-compose --profile mock up -d

# 查看日志
docker-compose logs -f agent-mock
```

### 测试API

**在浏览器中打开**:  
http://localhost:8765/docs

或使用curl:

```bash
# 健康检查
curl http://localhost:8765/health

# 查看工具
curl http://localhost:8765/tools

# 查看股票列表
curl http://localhost:8765/stocks
```

---

## 🎮 交互式测试

访问 **Swagger UI** 进行交互式测试：

**地址**: http://localhost:8765/docs

在Swagger UI中：
1. 找到 `POST /chat` 端点
2. 点击 "Try it out"
3. 输入查询，例如：
   ```json
   {
     "query": "比亚迪现在多少钱？"
   }
   ```
4. 点击 "Execute"
5. 查看响应

---

## ✅ 预期结果

### 健康检查
```json
{
  "status": "healthy",
  "agent_ready": true
}
```

### 工具列表
```json
{
  "count": 5,
  "tools": [
    {"name": "get_stock_price", ...},
    {"name": "get_technical_indicators", ...},
    {"name": "get_stock_history", ...},
    {"name": "compare_stocks", ...},
    {"name": "analyze_stock", ...}
  ]
}
```

### 股票列表
```json
{
  "count": 50,
  "stocks": [
    {"name": "比亚迪", "code": "002594"},
    {"name": "贵州茅台", "code": "600519"},
    ...
  ]
}
```

---

## 🔧 故障排查

### 问题1：Docker未运行

**错误**: `Cannot connect to the Docker daemon`

**解决**: 启动Docker Desktop

### 问题2：端口被占用

**错误**: `port is already allocated`

**解决**: 
1. 修改 `docker-compose.yml` 中的端口映射
2. 或停止占用8765端口的其他服务

### 问题3：容器启动失败

**排查步骤**:
```bash
# 查看日志
docker-compose logs agent-mock

# 检查容器状态
docker ps -a

# 重新构建
docker-compose --profile mock down
docker-compose --profile mock up -d --build
```

---

## 🎯 下一步

测试成功后，你可以：

1. **尝试GPU版本**:
   ```bash
   # 下载模型
   python scripts/download_model.py --model chatglm3-6b-int4
   
   # 修改配置
   编辑 server/configs/server_config.yaml
   
   # 构建GPU镜像
   ./docker_build.bat  # 选择选项2
   ```

2. **部署到生产环境**:
   - 查看 [DOCKER_GUIDE.md](./DOCKER_GUIDE.md)

3. **使用CLI客户端**:
   ```bash
   python start_client.py
   ```

4. **API集成**:
   - 查看 [USAGE_GUIDE.md](./USAGE_GUIDE.md)

---

## 📊 性能参考

| 指标 | Mock模式 | GPU模式 |
|------|---------|---------|
| 镜像大小 | ~600MB | ~2GB |
| 启动时间 | ~3秒 | ~10秒 |
| 响应时间 | <500ms | 1-2秒 |
| 内存占用 | ~200MB | ~5GB |
| GPU显存 | 0GB | 4-5GB |

---

**完整测试报告**: [DOCKER_TEST_REPORT.md](./DOCKER_TEST_REPORT.md)

**模型选择指南**: [MODEL_GUIDE.md](./MODEL_GUIDE.md)
