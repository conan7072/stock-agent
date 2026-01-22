# 模型选择指南

**硬件参考**：RTX 3070 8GB显存

---

## 🎯 推荐模型（按显存需求）

### 1. ChatGLM3-6B INT4 ⭐ 最推荐

| 项目 | 说明 |
|------|------|
| **显存需求** | 4-5GB |
| **模型文件** | ~13GB |
| **速度** | 15-20 tokens/s |
| **质量** | 优秀 |
| **并发** | 支持2-3人 |
| **适合显卡** | RTX 3070 8GB ✅ |

**下载命令**：
```bash
python scripts/download_model.py --model chatglm3-6b-int4
```

**配置**：
```yaml
model:
  name: chatglm3-6b
  path: ./models/chatglm3-6b
  quantization: int4
  device: cuda
  max_length: 4096
```

---

### 2. Qwen2-7B INT4

| 项目 | 说明 |
|------|------|
| **显存需求** | 5-6GB |
| **模型文件** | ~14GB |
| **速度** | 12-18 tokens/s |
| **质量** | 优秀 |
| **并发** | 支持1-2人 |
| **适合显卡** | RTX 3070 8GB ✅ |

**下载命令**：
```bash
python scripts/download_model.py --model qwen2-7b-int4
```

**配置**：
```yaml
model:
  name: qwen2-7b
  path: ./models/qwen2-7b
  quantization: int4
  device: cuda
  max_length: 4096
```

---

### 3. Qwen2-1.5B FP16 🚀 最快

| 项目 | 说明 |
|------|------|
| **显存需求** | 2-3GB |
| **模型文件** | ~3GB |
| **速度** | 30-40 tokens/s |
| **质量** | 良好 |
| **并发** | 支持4-5人 |
| **适合显卡** | RTX 3070 8GB ✅✅ |

**下载命令**：
```bash
python scripts/download_model.py --model qwen2-1.5b
```

**配置**：
```yaml
model:
  name: qwen2-1.5b
  path: ./models/qwen2-1.5b
  quantization: fp16
  device: cuda
  max_length: 4096
```

---

### 4. ChatGLM3-6B INT8

| 项目 | 说明 |
|------|------|
| **显存需求** | 6-7GB |
| **模型文件** | ~6.5GB |
| **速度** | 10-15 tokens/s |
| **质量** | 非常优秀 |
| **并发** | 支持1人 |
| **适合显卡** | RTX 3070 8GB ⚠️ 紧张 |

**下载命令**：
```bash
python scripts/download_model.py --model chatglm3-6b-int8
```

**配置**：
```yaml
model:
  name: chatglm3-6b
  path: ./models/chatglm3-6b
  quantization: int8
  device: cuda
  max_length: 4096
```

---

### 5. Mock LLM 💻 无GPU

| 项目 | 说明 |
|------|------|
| **显存需求** | 0GB |
| **模型文件** | 0GB |
| **速度** | 即时 |
| **质量** | 模拟（模板响应） |
| **并发** | 无限制 |
| **适合场景** | 开发测试 |

**配置**：
```yaml
model:
  mock_mode: true
  name: mock
```

---

## 📊 显存需求详解

### RTX 3070 8GB 显存分配

```
总显存: 8GB
├── 系统占用: 0.5-1GB
├── 模型加载: 4-5GB (INT4)
├── 推理缓存: 1-2GB
└── 剩余可用: 1-1.5GB
```

### 不同量化方式对比

| 量化方式 | 显存占用 | 质量损失 | 速度 |
|---------|---------|---------|------|
| **FP16** | 12GB | 0% | 基准 |
| **INT8** | 6-7GB | ~2% | +20% |
| **INT4** | 4-5GB | ~5% | +40% |
| **INT2** | 2-3GB | ~15% | +60% |

---

## 🎯 推荐配置（RTX 3070 8GB）

### 场景1：追求质量（单用户）

```yaml
model:
  name: chatglm3-6b
  quantization: int4
  max_length: 4096
  concurrent_users: 1
```

**预期性能**：
- 响应速度：15-20 tokens/s
- 质量：优秀
- 并发：1人

---

### 场景2：平衡性能（2-3用户）

```yaml
model:
  name: chatglm3-6b
  quantization: int4
  max_length: 2048  # 减少长度
  concurrent_users: 2
```

**预期性能**：
- 响应速度：12-18 tokens/s
- 质量：优秀
- 并发：2-3人

---

### 场景3：追求速度（多用户）

```yaml
model:
  name: qwen2-1.5b
  quantization: fp16
  max_length: 4096
  concurrent_users: 4
```

**预期性能**：
- 响应速度：30-40 tokens/s
- 质量：良好
- 并发：4-5人

---

## 🔧 配置方法

### 方式1：修改配置文件

编辑 `server/configs/server_config.yaml`：

```yaml
model:
  mock_mode: false      # 使用真实模型
  name: chatglm3-6b     # 模型名称
  path: ./models/chatglm3-6b  # 模型路径
  device: cuda          # 使用GPU
  quantization: int4    # 量化方式
  max_length: 4096      # 最大长度
  temperature: 0.7      # 温度
  top_p: 0.9           # Top-p采样
```

### 方式2：环境变量

```bash
export MODEL_NAME=chatglm3-6b
export MODEL_QUANTIZATION=int4
export MODEL_MAX_LENGTH=4096

python start_server.py
```

---

## 📥 模型下载

### 使用下载脚本（推荐）

```bash
# ChatGLM3-6B INT4（推荐）
python scripts/download_model.py --model chatglm3-6b-int4

# Qwen2-7B INT4
python scripts/download_model.py --model qwen2-7b-int4

# Qwen2-1.5B（最快）
python scripts/download_model.py --model qwen2-1.5b
```

### 手动下载

从Hugging Face或ModelScope下载：

```bash
# 使用国内镜像（更快）
export HF_ENDPOINT=https://hf-mirror.com

# ChatGLM3-6B
git clone https://hf-mirror.com/THUDM/chatglm3-6b ./models/chatglm3-6b

# Qwen2-7B
git clone https://hf-mirror.com/Qwen/Qwen2-7B-Instruct ./models/qwen2-7b

# Qwen2-1.5B
git clone https://hf-mirror.com/Qwen/Qwen2-1.5B-Instruct ./models/qwen2-1.5b
```

---

## ⚙️ 性能优化

### 1. 减少max_length

```yaml
max_length: 2048  # 从4096减到2048
```

**效果**：节省1-2GB显存，支持更多并发

### 2. 启用Flash Attention

```yaml
use_flash_attention: true
```

**效果**：速度提升20-30%，显存减少10-15%

### 3. 调整batch size

```yaml
batch_size: 1  # 单用户
# batch_size: 2  # 2-3用户
```

### 4. 限制并发数

```python
# server/src/api/main.py
MAX_CONCURRENT_REQUESTS = 2  # RTX 3070 8GB建议2-3
```

---

## 🧪 测试性能

### 测试脚本

```bash
# 测试生成速度
python scripts/benchmark_model.py --model chatglm3-6b

# 测试显存占用
python scripts/check_vram.py

# 压力测试
python scripts/stress_test.py --users 3 --duration 300
```

### 性能基准（RTX 3070 8GB）

| 模型 | 首Token | 生成速度 | 显存 | 并发 |
|------|--------|---------|------|------|
| ChatGLM3-6B INT4 | 1.2s | 18 t/s | 4.5GB | 2-3 |
| Qwen2-7B INT4 | 1.5s | 15 t/s | 5.5GB | 1-2 |
| Qwen2-1.5B FP16 | 0.5s | 35 t/s | 2.5GB | 4-5 |

---

## 🎯 最终推荐（RTX 3070 8GB）

### 首选：ChatGLM3-6B INT4

**原因**：
- ✅ 显存占用合理（4-5GB）
- ✅ 质量优秀
- ✅ 速度足够快（15-20 t/s）
- ✅ 支持2-3人并发
- ✅ 中文效果好

**配置**：
```yaml
model:
  mock_mode: false
  name: chatglm3-6b
  path: ./models/chatglm3-6b
  device: cuda
  quantization: int4
  max_length: 4096
```

---

## ❓ 常见问题

### Q1: 13GB模型文件为什么只需要4GB显存？

A: 13GB是原始FP16模型大小，INT4量化后：
- 模型参数从16bit压缩到4bit
- 实际加载到显存约4-5GB
- 推理时需要额外1-2GB缓存

### Q2: 如何知道当前显存使用？

```bash
# Windows
nvidia-smi

# Python
python -c "import torch; print(torch.cuda.memory_allocated() / 1024**3)"
```

### Q3: 显存不够怎么办？

1. 减小max_length（4096→2048）
2. 使用更小模型（Qwen2-1.5B）
3. 降低并发数
4. 使用CPU（慢但可用）

### Q4: 可以同时加载多个模型吗？

A: 不推荐。RTX 3070 8GB只够加载1个模型。
可以通过配置切换不同模型。

---

**开始选择适合你的模型吧！** 🚀
