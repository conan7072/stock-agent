# 🎮 立即试用 - 股票咨询Agent

**当前状态**: ✅ 服务正在运行！  
**容器**: stock-agent-mock (健康)  
**端口**: http://localhost:8765

---

## 🌐 方式1：使用Swagger UI（最简单）

### 步骤1：打开浏览器

访问: **http://localhost:8765/docs**

### 步骤2：测试聊天接口

1. 找到 `POST /chat` 端点
2. 点击 "Try it out"
3. 输入以下查询之一：

```json
{"query": "比亚迪现在多少钱？"}
```

```json
{"query": "分析一下贵州茅台"}
```

```json
{"query": "比较比亚迪和特斯拉"}
```

```json
{"query": "什么是MACD指标？"}
```

4. 点击 "Execute"
5. 查看响应

---

## 💻 方式2：使用PowerShell

### 测试健康检查

```powershell
Invoke-RestMethod -Uri http://localhost:8765/health | ConvertTo-Json
```

**预期输出**:
```json
{
  "status": "healthy",
  "agent_ready": true
}
```

---

### 查询股票价格

```powershell
$body = '{"query":"比亚迪现在多少钱？"}' 
$response = Invoke-RestMethod -Uri http://localhost:8765/chat -Method Post -Body $body -ContentType "application/json"
$response.answer
```

---

### 获取工具列表

```powershell
Invoke-RestMethod -Uri http://localhost:8765/tools | ConvertTo-Json -Depth 5
```

**预期输出**:
```json
{
  "tools": [
    {
      "name": "get_stock_price",
      "description": "获取指定股票的最新价格、成交量等行情信息..."
    },
    ...
  ],
  "count": 5
}
```

---

### 获取股票列表

```powershell
$stocks = Invoke-RestMethod -Uri http://localhost:8765/stocks
"共有 $($stocks.count) 只股票"
$stocks.stocks | Select-Object -First 10 | Format-Table
```

**预期输出**:
```
共有 50 只股票

name         code
----         ----
万科A        000002
三一重工     600031
上海机场     600009
东方财富     300059
...
```

---

## 🐍 方式3：使用Python

### 安装依赖

```bash
pip install requests
```

### 测试脚本

```python
import requests
import json

# 基础URL
BASE_URL = "http://localhost:8765"

# 1. 健康检查
print("=" * 60)
print("健康检查")
print("=" * 60)
response = requests.get(f"{BASE_URL}/health")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 2. 查询股票
print("\n" + "=" * 60)
print("查询股票价格")
print("=" * 60)
response = requests.post(
    f"{BASE_URL}/chat",
    json={"query": "比亚迪现在多少钱？"}
)
result = response.json()
print(f"问题: 比亚迪现在多少钱？")
print(f"回答: {result['answer'][:200]}...")

# 3. 技术分析
print("\n" + "=" * 60)
print("技术分析")
print("=" * 60)
response = requests.post(
    f"{BASE_URL}/chat",
    json={"query": "分析一下贵州茅台的技术指标"}
)
result = response.json()
print(f"问题: 分析一下贵州茅台的技术指标")
print(f"回答: {result['answer'][:200]}...")

# 4. 知识问答
print("\n" + "=" * 60)
print("知识问答")
print("=" * 60)
response = requests.post(
    f"{BASE_URL}/chat",
    json={"query": "什么是MACD指标？"}
)
result = response.json()
print(f"问题: 什么是MACD指标？")
print(f"回答: {result['answer'][:200]}...")

# 5. 股票对比
print("\n" + "=" * 60)
print("股票对比")
print("=" * 60)
response = requests.post(
    f"{BASE_URL}/chat",
    json={"query": "比较比亚迪和宁德时代"}
)
result = response.json()
print(f"问题: 比较比亚迪和宁德时代")
print(f"回答: {result['answer'][:200]}...")

# 6. 获取工具列表
print("\n" + "=" * 60)
print("工具列表")
print("=" * 60)
response = requests.get(f"{BASE_URL}/tools")
tools = response.json()
print(f"共有 {tools['count']} 个工具:")
for tool in tools['tools']:
    print(f"  - {tool['name']}: {tool['description'][:50]}...")

# 7. 获取股票列表
print("\n" + "=" * 60)
print("股票列表")
print("=" * 60)
response = requests.get(f"{BASE_URL}/stocks")
stocks = response.json()
print(f"共有 {stocks['count']} 只股票:")
for stock in stocks['stocks'][:10]:
    print(f"  - {stock['name']} ({stock['code']})")
print("  ...")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
```

保存为 `test_docker_api.py` 并运行：

```bash
python test_docker_api.py
```

---

## 🎯 方式4：使用CLI客户端

### 启动交互式客户端

```bash
python start_client.py
```

### 使用示例

```
欢迎使用股票咨询Agent！

您: 比亚迪现在多少钱？

Agent: 根据最新数据，比亚迪(002594)当前价格为...

您: 分析一下贵州茅台

Agent: 贵州茅台(600519)综合分析如下：
1. 基本行情：...
2. 技术指标：...
3. 趋势判断：...

您: exit

再见！
```

---

## 📋 可以尝试的问题

### 价格查询类

- "比亚迪现在多少钱？"
- "贵州茅台的价格是多少？"
- "查询宁德时代的股价"

### 技术分析类

- "分析一下比亚迪的技术指标"
- "贵州茅台的MACD怎么样？"
- "宁德时代的RSI是多少？"

### 历史数据类

- "比亚迪最近一个月的走势"
- "贵州茅台近期表现如何？"
- "宁德时代最近涨了还是跌了？"

### 对比分析类

- "比较比亚迪和宁德时代"
- "贵州茅台和五粮液哪个好？"
- "对比一下三大新能源车企"

### 综合分析类

- "全面分析比亚迪"
- "贵州茅台值得投资吗？"
- "给我分析一下宁德时代"

### 知识问答类

- "什么是MACD指标？"
- "如何看布林带？"
- "RSI指标怎么用？"
- "什么是均线？"

---

## 🔍 查看实时日志

```bash
# 查看最新日志
docker-compose logs -f agent-mock

# 查看最近50行
docker-compose logs --tail=50 agent-mock
```

---

## 🛑 停止服务

```bash
docker-compose --profile mock down
```

---

## 🔄 重启服务

```bash
# 停止
docker-compose --profile mock down

# 启动
docker-compose --profile mock up -d

# 查看状态
docker ps
```

---

## 📊 性能监控

### 查看容器资源使用

```bash
docker stats stock-agent-mock
```

**输出示例**:
```
CONTAINER ID   NAME               CPU %     MEM USAGE / LIMIT     MEM %
09820c307dbc   stock-agent-mock   0.50%     200MiB / 15.41GiB    1.27%
```

---

## 🎓 进阶使用

### 1. 流式响应

```python
import requests

response = requests.post(
    "http://localhost:8765/chat/stream",
    json={"query": "分析比亚迪"},
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

### 2. 批量查询

```python
questions = [
    "比亚迪现在多少钱？",
    "贵州茅台的价格是多少？",
    "宁德时代的技术指标如何？",
    "比较比亚迪和宁德时代"
]

for q in questions:
    response = requests.post(
        "http://localhost:8765/chat",
        json={"query": q}
    )
    print(f"Q: {q}")
    print(f"A: {response.json()['answer'][:100]}...")
    print("-" * 60)
```

### 3. 错误处理

```python
try:
    response = requests.post(
        "http://localhost:8765/chat",
        json={"query": "测试"},
        timeout=10
    )
    response.raise_for_status()
    result = response.json()
    
    if result['success']:
        print(result['answer'])
    else:
        print(f"错误: {result['error']}")
        
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.ConnectionError:
    print("连接失败，请检查服务是否启动")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 💡 提示

1. **首次查询可能较慢**: Agent需要加载数据和初始化
2. **Mock模式限制**: 使用模板响应，不是真实LLM推理
3. **中文显示问题**: PowerShell可能显示乱码，建议使用Swagger UI
4. **端口冲突**: 如果8765被占用，修改 `docker-compose.yml`

---

## 🎉 享受你的股票咨询Agent！

**当前运行状态**: ✅ 健康  
**API文档**: http://localhost:8765/docs  
**健康检查**: http://localhost:8765/health

**需要帮助？** 查看完整文档：
- [USAGE_GUIDE.md](./USAGE_GUIDE.md)
- [DOCKER_GUIDE.md](./DOCKER_GUIDE.md)
- [QUICK_DOCKER_TEST.md](./QUICK_DOCKER_TEST.md)
