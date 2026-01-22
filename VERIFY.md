# 项目验证指南

## 当前状态
- ✅ 项目框架已搭建
- ✅ 配置文件已创建
- ✅ 数据准备脚本已完成
- ⏳ 等待验证和测试

---

## 验证方案（适合显存不足的机器）

### 阶段1：无需GPU的组件验证 ⭐ 推荐先做

这些测试不需要显卡，可以在当前机器完成：

#### 步骤1：创建虚拟环境

```powershell
# Windows PowerShell
cd c:\project\agent
.\setup_venv.ps1

# 或手动创建
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
```

#### 步骤2：安装轻量级依赖（不含PyTorch）

```powershell
# 激活环境
venv\Scripts\activate

# 只安装数据处理相关
pip install pandas pyarrow akshare pyyaml rich typer
```

#### 步骤3：下载股票数据 ✅ 可验证

```powershell
python scripts\download_stock_data.py
```

**预期结果**：
- 下载50只股票的历史数据
- 保存到 `data/stocks/` 目录
- 约20MB数据
- 每只股票有1000-1500条记录

**验证成功标志**：
```
✅ 成功: 40-50 只
📁 数据位置: c:\project\agent\data\stocks
💾 总大小: 15-25 MB
```

#### 步骤4：检查知识库文件 ✅ 可验证

```powershell
# 查看知识库文件
dir data\knowledge\basics\
dir data\knowledge\terms\
dir data\knowledge\faq\

# 或使用Python检查
python -c "from pathlib import Path; kb = Path('data/knowledge'); print(f'知识库文件: {len(list(kb.rglob(\"*.md\")))} 个'); print(f'总大小: {sum(f.stat().st_size for f in kb.rglob(\"*.md\")) / 1024:.1f} KB')"
```

**预期结果**：
```
知识库文件: 4 个
总大小: 40-60 KB
```

#### 步骤5：测试配置加载

创建测试脚本：

```powershell
# 创建测试文件
@"
import yaml
from pathlib import Path

config_file = Path('server/configs/server_config.yaml')
with open(config_file, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

print('✅ 配置文件加载成功')
print(f'服务端口: {config[\"server\"][\"port\"]}')
print(f'模型名称: {config[\"model\"][\"name\"]}')
print(f'RAG启用: {config[\"rag\"][\"enabled\"]}')
"@ | Out-File -Encoding utf8 test_config.py

python test_config.py
```

#### 步骤6：构建向量数据库 ⚠️ 需要安装更多依赖

```powershell
# 安装RAG相关依赖
pip install langchain langchain-community sentence-transformers chromadb

# 构建向量数据库（使用CPU）
python scripts\build_vectordb.py
```

**预期结果**：
- 自动下载 bge-small-zh-v1.5 模型（约90MB）
- 向量化4个知识库文件
- 生成约100-200个文档块
- 保存到 `data/vector_db/` 目录

**注意**：这一步会在CPU上运行，速度较慢（2-5分钟），但可以完成。

---

### 阶段2：需要GPU的组件（延后到有显卡的机器）

这些需要在有3070显卡的机器上测试：

#### 模型下载和加载

```powershell
# 下载ChatGLM3-6B（约13GB）
python scripts\download_model.py

# 测试模型加载
python -c "from transformers import AutoTokenizer, AutoModel; tokenizer = AutoTokenizer.from_pretrained('./models/chatglm3-6b', trust_remote_code=True); model = AutoModel.from_pretrained('./models/chatglm3-6b', trust_remote_code=True).quantize(4).cuda(); print('✅ 模型加载成功')"
```

---

## 快速验证命令（无需GPU）

如果只想快速验证框架是否正常：

```powershell
# 1. 激活环境
venv\Scripts\activate

# 2. 安装最小依赖
pip install pandas pyyaml rich

# 3. 运行环境检查（会跳过GPU检查）
python scripts\setup_env.py

# 4. 查看项目结构
python -c "from pathlib import Path; import json; def tree(p, prefix='', max_depth=2, depth=0): print(prefix + p.name + ('/
' if p.is_dir() else '')); if depth < max_depth and p.is_dir(): for i, child in enumerate(sorted(p.iterdir())[:5]): tree(child, prefix + '  ', max_depth, depth+1); tree(Path('.'), max_depth=2)"
```

---

## 常见问题

### Q1: PyTorch DLL加载失败怎么办？
A: 这是常见问题，通常是因为：
1. **CUDA版本不匹配**：卸载重装对应版本
2. **缺少VC++运行库**：下载安装 Microsoft Visual C++ Redistributable

**解决方案**（如果需要GPU）：
```powershell
# 卸载旧版本
pip uninstall torch torchvision torchaudio

# 安装CUDA 11.8版本（适配3070）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**如果只是测试（CPU够用）**：
```powershell
# 安装CPU版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Q2: 显存不够怎么办？
A: 三种方案：
1. **使用更小的模型**：Qwen2-1.5B（只需1.5GB）
2. **CPU模式**：慢但可以测试功能
3. **Mock LLM**：创建假的LLM响应，测试其他组件

### Q3: 能否在当前机器测试除LLM外的所有功能？
A: **可以！** 使用Mock模式：

```python
# 创建 server/src/llm/mock_llm.py
class MockChatGLM:
    def __init__(self):
        self.name = "MockChatGLM"
    
    def generate(self, prompt, **kwargs):
        return "这是一个模拟响应，用于测试。[Mock Response]"

# 在配置中启用Mock模式
# server_config.yaml:
# model:
#   mock_mode: true
```

这样可以测试：
- ✅ 数据加载
- ✅ 工具调用
- ✅ RAG检索
- ✅ API服务
- ✅ CLI客户端
- ✅ Agent工作流

### Q4: 当前机器可以完成哪些开发？
A: **几乎所有**！除了LLM推理，其他都可以：
- ✅ 开发工具函数（股票数据查询）
- ✅ 开发RAG检索逻辑
- ✅ 开发Agent工作流（使用Mock LLM）
- ✅ 开发FastAPI服务
- ✅ 开发CLI客户端
- ✅ 编写单元测试
- ✅ 编写集成测试

只有在最后部署时，才需要有显卡的机器。

---

## 推荐的验证流程（当前机器）

```powershell
# 第1步：基础验证（5分钟）
venv\Scripts\activate
pip install pandas pyyaml rich
python scripts\setup_env.py

# 第2步：数据验证（10分钟）
pip install akshare pyarrow
python scripts\download_stock_data.py

# 第3步：RAG验证（5分钟，可选）
pip install langchain langchain-community sentence-transformers chromadb
python scripts\build_vectordb.py

# 完成！✅
```

**然后可以选择**：
- A) 继续在当前机器开发（使用Mock LLM）
- B) 等待部署到有显卡的机器再继续
- C) 先开发不依赖LLM的组件（工具、API、客户端）

---

## 下一步建议

### 方案A：继续在当前机器开发 ⭐ 推荐

1. 完成阶段1的验证
2. 我帮您创建Mock LLM
3. 开发和测试其他组件
4. 最后迁移到3070机器，替换真实LLM

**优点**：不被硬件限制，可以持续开发

### 方案B：只做验证，等待迁移

1. 完成阶段1的验证
2. 确保数据和配置正确
3. 将项目打包迁移到3070机器
4. 在目标机器上继续开发

**优点**：最终环境一致，减少适配问题

---

**您倾向哪个方案？** 我可以相应地调整开发策略。
