# 股票咨询Agent使用指南

**版本**: 1.0.0  
**更新**: 2026-01-21  
**状态**: ✅ 开发完成

---

## 📋 目录

1. [快速开始](#快速开始)
2. [独立模式（无需服务器）](#独立模式)
3. [服务器-客户端模式](#服务器客户端模式)
4. [API使用](#api使用)
5. [常见问题](#常见问题)
6. [故障排除](#故障排除)

---

## 🚀 快速开始

### 方式1：独立测试（最简单）

直接测试Agent，无需启动服务器：

```bash
# 测试Agent
python test_agent.py

# 选择模式2进入交互
```

**适合场景**：本地测试、开发调试

---

## 🖥️ 独立模式

### 测试工具

```bash
# 测试5个股票工具
python test_tools.py
```

### 测试RAG系统

```bash
# 测试知识库检索
python test_rag.py
```

### 测试Agent

```bash
# 测试Agent（自动测试）
python test_agent.py
# 选择1 - 运行自动测试

# 交互模式
python test_agent.py
# 选择2 - 进入交互模式
```

**功能**：
- ✅ 价格查询
- ✅ 技术指标分析
- ✅ 股票对比
- ✅ 知识查询
- ✅ 历史数据

---

## 🌐 服务器-客户端模式

适合局域网多用户使用，一台机器运行服务器，其他机器通过客户端连接。

### 步骤1：启动服务器

在有GPU的机器上（或使用Mock模式的任何机器）：

```bash
python start_server.py
```

**输出**：
```
============================================================
启动股票咨询Agent服务...
============================================================

Agent初始化完成：LLM=MockLLM, 工具数=5

服务已启动:
  - Host: 0.0.0.0
  - Port: 8765
  - API Docs: http://0.0.0.0:8765/docs
============================================================
```

**说明**：
- 默认监听所有IP（0.0.0.0）
- 端口：8765
- 可通过配置文件修改：`server/configs/server_config.yaml`

### 步骤2：启动客户端

在任何机器上（同一局域网）：

```bash
# 连接到本地服务器
python start_client.py

# 连接到远程服务器
python start_client.py http://192.168.1.100:8765
```

**使用示例**：

```
======================================================================
                    股票咨询Agent系统
======================================================================

命令列表:
  - 直接输入问题进行咨询（如：比亚迪现在多少钱？）
  - /help  - 显示帮助
  - /tools - 显示可用工具
  - /stocks - 显示支持的股票
  - /quit 或 /exit - 退出

----------------------------------------------------------------------

连接服务器...
[OK] 服务器连接成功

======================================================================

开始对话吧！输入 /help 查看帮助

您: 比亚迪现在多少钱？

[Agent正在思考...]

Agent: 根据分析，比亚迪的情况如下：

**价格走势**
最近一个月比亚迪呈现震荡上行的态势，整体表现相对稳健...

（完整回答）

----------------------------------------------------------------------

您: /stocks

获取股票列表...

支持的股票 (共49只):
----------------------------------------------------------------------
  比亚迪(002594)  宁德时代(300750)  贵州茅台(600519)
  中国平安(601318)  招商银行(600036)  ...
----------------------------------------------------------------------

您: /quit

再见！
```

---

## 🔌 API使用

### 测试API

```bash
# 确保服务器已启动
python start_server.py

# 在另一个终端运行测试
python test_api.py
```

### API端点

#### 1. 健康检查

```bash
GET /health
```

**响应**：
```json
{
  "status": "healthy",
  "agent_ready": true
}
```

#### 2. 聊天接口（非流式）

```bash
POST /chat
```

**请求**：
```json
{
  "query": "比亚迪现在多少钱？",
  "stream": false
}
```

**响应**：
```json
{
  "answer": "根据分析，比亚迪...",
  "success": true,
  "error": null
}
```

#### 3. 流式聊天

```bash
POST /chat/stream
```

**说明**：返回Server-Sent Events (SSE)流式数据

#### 4. 工具列表

```bash
GET /tools
```

**响应**：
```json
{
  "tools": [
    {
      "name": "get_stock_price",
      "description": "获取指定股票的最新价格..."
    },
    ...
  ],
  "count": 5
}
```

#### 5. 股票列表

```bash
GET /stocks
```

**响应**：
```json
{
  "stocks": [
    {"name": "比亚迪", "code": "002594"},
    {"name": "宁德时代", "code": "300750"},
    ...
  ],
  "count": 49
}
```

### Python API调用示例

```python
import requests

# 健康检查
response = requests.get("http://localhost:8765/health")
print(response.json())

# 聊天
response = requests.post(
    "http://localhost:8765/chat",
    json={"query": "比亚迪现在多少钱？"}
)
data = response.json()
print(data['answer'])
```

### cURL示例

```bash
# 健康检查
curl http://localhost:8765/health

# 聊天
curl -X POST http://localhost:8765/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "比亚迪现在多少钱？"}'

# 工具列表
curl http://localhost:8765/tools

# 股票列表
curl http://localhost:8765/stocks
```

---

## ❓ 常见问题

### Q1: 如何切换到真实GPU模式？

**答**：修改 `server/configs/server_config.yaml`：

```yaml
model:
  mock_mode: false  # 改为false
  device: cuda      # 使用GPU
  path: ./models/chatglm3-6b  # 模型路径
```

### Q2: 如何添加更多股票？

**答**：修改 `scripts/download_stock_data.py` 中的股票列表，重新运行：

```bash
python scripts/download_stock_data.py
```

### Q3: 如何修改服务器端口？

**答**：修改 `server/configs/server_config.yaml`：

```yaml
server:
  port: 9999  # 改为你想要的端口
```

### Q4: 客户端如何连接局域网服务器？

**答**：

```bash
# 服务器IP是192.168.1.100，端口8765
python start_client.py http://192.168.1.100:8765
```

### Q5: 支持哪些查询类型？

**答**：

1. **价格查询**
   - "比亚迪现在多少钱？"
   - "宁德时代的股价是多少？"

2. **技术指标**
   - "贵州茅台的技术指标怎么样？"
   - "中国平安的MACD指标如何？"

3. **历史数据**
   - "招商银行最近5天的表现"
   - "比亚迪近期走势"

4. **股票对比**
   - "对比一下比亚迪和宁德时代"
   - "比较新能源龙头股"

5. **综合分析**
   - "分析一下中国平安"
   - "贵州茅台怎么样？"

6. **知识查询**
   - "什么是MACD指标？"
   - "如何看均线？"
   - "什么是市盈率？"

---

## 🔧 故障排除

### 问题1：无法启动服务器

**症状**：`python start_server.py` 报错

**解决**：

1. 检查配置文件：
```bash
# 确认文件存在
ls server/configs/server_config.yaml
```

2. 检查端口占用：
```bash
# Windows
netstat -ano | findstr 8765

# Linux
lsof -i :8765
```

3. 修改端口或停止占用端口的程序

### 问题2：客户端无法连接

**症状**：`[错误] 无法连接到服务器`

**解决**：

1. 确认服务器已启动
2. 检查防火墙：
   - Windows：允许端口8765
   - Linux：`sudo ufw allow 8765`
3. ping测试连通性：
```bash
ping 服务器IP
```

### 问题3：响应很慢

**症状**：查询等待时间长

**解决**：

1. **Mock模式**：已经很快，检查网络延迟
2. **GPU模式**：
   - 检查显存占用
   - 降低`max_length`
   - 减小batch size

### 问题4：中文乱码

**症状**：输出显示乱码

**解决**：

Windows PowerShell：
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python start_client.py
```

或使用Windows Terminal（推荐）

### 问题5：找不到模块

**症状**：`ModuleNotFoundError`

**解决**：

```bash
# 安装依赖
pip install -r requirements.txt

# 或分别安装
cd server
pip install -r requirements.txt

cd ../client
pip install -r requirements.txt
```

---

## 📚 更多资源

- **项目文档**：
  - [PLAN.md](./PLAN.md) - 技术实现计划
  - [STATUS.md](./STATUS.md) - 当前状态
  - [TOOLS_GUIDE.md](./TOOLS_GUIDE.md) - 工具使用指南
  - [tracker.md](./tracker.md) - 开发进度

- **测试脚本**：
  - `test_tools.py` - 工具测试
  - `test_rag.py` - RAG测试
  - `test_agent.py` - Agent测试
  - `test_api.py` - API测试

- **启动脚本**：
  - `start_server.py` - 启动服务器
  - `start_client.py` - 启动客户端

- **数据脚本**：
  - `verify_data.py` - 验证数据
  - `example_tool_usage.py` - 工具使用示例

---

## 🎉 恭喜！

你已经掌握了股票咨询Agent的所有使用方法！

**下一步**：
- 尝试不同类型的查询
- 添加更多股票数据
- 在局域网部署服务器
- 集成到你的应用中

**享受使用吧！** 📈💰
