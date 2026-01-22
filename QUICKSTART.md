# 快速开始指南

## 🚀 无GPU版本（当前推荐）

### 1. 创建虚拟环境（2分钟）

```powershell
cd c:\project\agent

# 创建虚拟环境
python -m venv venv

# 激活环境
venv\Scripts\activate

# 升级pip
python -m pip install --upgrade pip
```

### 2. 安装基础依赖（3分钟）

```powershell
# 安装无GPU依赖（不含PyTorch）
pip install pydantic pydantic-settings pyyaml pandas pyarrow akshare rich typer
```

### 3. 测试Mock LLM（1分钟）

```powershell
# 运行LLM测试
python test_llm.py
```

**预期输出**：
```
🧪 测试Mock LLM（无需GPU）
📊 模型信息:
   model_name: MockLLM
   model_type: mock
   ...

📝 测试1: 基础文本生成
输入: 你好，请介绍一下你自己
输出: 这是一个很好的问题...

📈 测试2: 股票分析  
输入: 比亚迪股票最近表现怎么样？
输出: 根据分析，比亚迪的情况如下...

✅ Mock LLM测试完成！
```

### 4. 下载股票数据（5-10分钟）

```powershell
python scripts\download_stock_data.py
```

### 5. 构建向量数据库（5分钟，可选）

```powershell
# 安装RAG依赖
pip install langchain langchain-community sentence-transformers chromadb

# 构建向量库
python scripts\build_vectordb.py
```

---

## ✅ 验证成功标志

完成上述步骤后，您应该看到：

```
c:\project\agent\
├── venv\                    ✅ 虚拟环境
├── data\
│   ├── stocks\              ✅ 40-50个.parquet文件
│   ├── knowledge\           ✅ 4个.md文件
│   └── vector_db\           ✅ Chroma数据库文件
└── ...
```

---

## 🎯 当前可以做什么？

### ✅ 已经可以使用：
- Mock LLM（模拟智能响应）
- 股票数据查询（真实历史数据）
- 知识库（4个markdown文档）
- 向量检索（RAG系统）

### 🔜 接下来开发：
- 5个股票工具函数
- LangGraph Agent
- FastAPI服务
- CLI客户端

---

## 🔄 切换到真实GPU版本

当您迁移到有3070显卡的机器时：

### 步骤1：安装PyTorch（支持CUDA）

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 步骤2：安装Transformers

```powershell
pip install transformers accelerate sentencepiece cpm-kernels
```

### 步骤3：下载模型

```powershell
python scripts\download_model.py
```

### 步骤4：修改配置

编辑 `server/configs/server_config.yaml`:

```yaml
model:
  mock_mode: false  # 改为 false
  device: "cuda"    # 使用GPU
```

### 步骤5：重启服务

```powershell
python server\start_server.py
```

**就这么简单！** 其他代码完全不需要改动。

---

## 💡 开发建议

### 当前阶段（无GPU）：
1. ✅ 使用Mock LLM完成所有开发
2. ✅ 测试业务逻辑、API接口
3. ✅ 编写单元测试和集成测试
4. ✅ 开发客户端和工具

### 后续阶段（有GPU）：
1. 🔄 一键切换到真实模型
2. 🧪 测试真实推理效果
3. ⚡ 性能调优
4. 🚀 生产部署

---

## 🐛 常见问题

### Q: 如何确认当前使用的是Mock还是真实LLM？

A: 查看启动日志：
```
🎭 使用Mock LLM（无需GPU）  ← Mock模式
🤖 使用真实LLM: chatglm3-6b ← 真实模式
```

### Q: Mock LLM的响应质量如何？

A: Mock LLM的响应是预设的模板，足够用于：
- ✅ 开发和调试业务逻辑
- ✅ 测试API接口
- ✅ 验证工作流程
- ❌ 不适合评估最终效果

### Q: 真实LLM和Mock LLM性能差异？

| 指标 | Mock LLM | 真实LLM (3070) |
|------|---------|---------------|
| 首次响应 | 0.5秒 | 1-2秒 |
| 生成速度 | 即时 | 15-20 tokens/s |
| 显存占用 | 0 MB | 4-5 GB |
| 响应质量 | 模板 | 智能生成 |

---

## 📞 需要帮助？

- 📖 查看 [PLAN.md](PLAN.md) - 完整技术方案
- 📋 查看 [tracker.md](tracker.md) - 项目进度
- 🔍 查看 [VERIFY.md](VERIFY.md) - 详细验证指南

---

**下一步**：继续开发核心功能，或先运行测试验证当前进度。
