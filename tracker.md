# 项目进展追踪

**项目名称**：股票咨询Agent系统  
**创建时间**：2026-01-21  
**当前阶段**：规划完成，准备开发  

---

## 开发进度总览

```
Phase 1: 基础搭建         [██████████] 100% (第1-2周)
Phase 2: 核心功能         [███░░░░░░░] 33%  (第3-4周)
Phase 3: 服务化           [░░░░░░░░░░] 0%   (第5周)
Phase 4: 测试和部署       [░░░░░░░░░░] 0%   (第6周)
---------------------------------------------------
总体进度:                 [████░░░░░░] 40%
```

---

## 任务清单

### ✅ 已完成 (4/15)

#### Phase 1: 基础搭建
- [x] **env-setup** - 环境搭建：CUDA、Python虚拟环境、下载ChatGLM3-6B模型 ✅
- [x] **prepare-data** - 准备数据：用akshare下载49只股票历史数据，准备基础知识库文件 ✅
- [x] **llm-service** - 实现LLM服务：MockLLM（无GPU版本）、测试生成速度 ✅

#### Phase 2: 核心功能
- [x] **tools-impl** - 实现5个股票工具：get_stock_price、get_technical_indicators等，基于真实数据 ✅

### 🔄 进行中 (0/15)

无

### ⏳ 待开始 (11/15)
- [ ] **rag-system** - 搭建RAG系统：Chroma向量库、bge-small-zh嵌入、知识库导入
- [ ] **langgraph-agent** - 开发LangGraph Agent：定义状态图、实现各节点、集成工具和RAG

#### Phase 3: 服务化
- [ ] **fastapi-server** - 搭建FastAPI服务：端点实现（8765端口）、流式响应、WebSocket、认证
- [ ] **queue-concurrency** - 实现并发控制：请求队列、信号量、超时处理
- [ ] **cli-client** - 开发CLI客户端：httpx/websockets通信、rich界面、配置管理

#### Phase 4: 测试和部署
- [ ] **unit-tests** - 编写单元测试：工具、数据加载、RAG检索测试
- [ ] **integration-tests** - 编写集成测试：Agent工作流、API端点测试
- [ ] **load-tests** - 编写压力测试：Locust测试脚本、性能基准
- [ ] **docker-package** - Docker打包：Dockerfile、docker-compose、镜像导出脚本
- [ ] **install-scripts** - 编写安装脚本：Windows PowerShell和Linux Bash一键安装
- [ ] **documentation** - 编写文档：部署指南、API文档、开发指南

---

## 里程碑

| 里程碑 | 目标日期 | 状态 | 说明 |
|--------|---------|------|------|
| M1: 环境就绪 | 第1周末 | ⏳ 待开始 | 模型可加载，数据已准备 |
| M2: Agent可用 | 第3周末 | ⏳ 待开始 | 本地命令行可查询股票 |
| M3: 服务上线 | 第5周末 | ⏳ 待开始 | 服务端运行，客户端可连接 |
| M4: 生产就绪 | 第6周末 | ⏳ 待开始 | 测试完成，文档齐全，可部署 |

---

## 当前工作

**当前任务**：tools-impl - 股票工具实现（已完成） 
**负责人**：AI Assistant  
**开始时间**：2026-01-21  
**完成时间**：2026-01-21  

**工作内容**：
- ✅ 实现股票数据加载器（stock_loader.py）
- ✅ 实现技术指标计算模块（stock_analyzer.py）
  - MA均线（5/10/20/60日）
  - MACD指标
  - RSI指标
  - 布林带（BOLL）
  - 趋势分析
  - 支撑/压力位
  - 量比计算
- ✅ 实现5个股票工具（stock_tools.py）
  1. get_stock_price - 获取股票价格
  2. get_technical_indicators - 获取技术指标
  3. get_stock_history - 获取历史数据
  4. compare_stocks - 比较股票
  5. analyze_stock - 综合分析
- ✅ 编写测试套件（test_tools.py）- 100%通过
- ✅ 创建工具使用指南（TOOLS_GUIDE.md）
- ✅ 创建使用示例（example_tool_usage.py）

**测试结果**：
- ✅ 所有5个工具测试通过
- ✅ 支持49只真实股票数据
- ✅ 技术指标计算准确
- ✅ 数据加载性能良好

**下一步计划**：
- 搭建RAG系统（Chroma向量库、知识库查询）
- 开发LangGraph Agent（集成工具和RAG）
- 搭建FastAPI服务（API端点）

---

## 技术决策记录

### 2026-01-21 - 初始技术选型

**背景**：需要在RTX 3070 8GB显卡上运行股票咨询Agent

**决策**：
1. **模型选择**：ChatGLM3-6B INT4（4GB显存）而非Qwen2-7B（6GB）
   - 理由：留更多显存给并发和向量模型，支持3-4个并发用户
   
2. **Agent框架**：LangGraph + LangChain而非纯手写
   - 理由：成熟的工具调用支持，便于调试和维护
   
3. **数据源**：akshare历史数据而非纯模拟数据
   - 理由：基于真实数据，后期可无缝切换到实时API
   
4. **服务端口**：8765而非8000/8080
   - 理由：避免常用端口冲突
   
5. **部署方式**：服务端-客户端架构而非单机CLI
   - 理由：局域网多机器共享GPU资源

**影响**：
- 显存占用更低，并发能力更强
- 开发效率提升，代码可维护性更好
- 数据更真实，用户体验更好

---

## 变更日志

### 2026-01-21

#### 晚上 - 股票工具实现完成 ✅
- [完成] ✅ tools-impl任务
  - 实现股票数据加载器（支持名称/代码查询、缓存机制）
  - 实现技术指标计算（MA、MACD、RSI、BOLL、趋势、支撑压力、量比）
  - 实现5个股票工具：
    1. get_stock_price（获取最新价格）
    2. get_technical_indicators（技术指标分析）
    3. get_stock_history（历史数据查询）
    4. compare_stocks（多股票对比）
    5. analyze_stock（综合分析）
  - 编写完整测试套件（100%通过）
  - 创建TOOLS_GUIDE.md工具使用指南
  - 创建example_tool_usage.py使用示例
  - 修复Windows编码问题（移除emoji字符）

#### 下午 - 数据准备和LLM服务 ✅
- [完成] ✅ prepare-data任务
  - 下载49只热门A股数据（2020-2026，约1400条/股）
  - 创建知识库文件（股票基础、技术分析、术语、FAQ）
  - 构建简化版向量数据库（关键词匹配）
  - 创建数据验证脚本（verify_data.py）
- [完成] ✅ llm-service任务
  - 实现MockLLM（无GPU开发版本）
  - 创建LLM工厂模式（支持多种LLM）
  - 测试通过（test_llm.py）

#### 上午 - 环境搭建完成 ✅
- [完成] ✅ env-setup任务
  - 创建完整项目目录结构
  - 编写requirements.txt（3个版本：总的、服务端、客户端）
  - 创建.gitignore配置
  - 编写server_config.yaml配置文件
  - 创建README.md项目文档
  - 编写setup_venv.ps1和setup_venv.sh虚拟环境设置脚本
  - 编写scripts/download_model.py模型下载脚本（支持HF-Mirror镜像）
  - 编写scripts/setup_env.py环境检查脚本
  - 创建所有必要的__init__.py文件

#### 清晨 - 项目初始化
- [初始化] 创建项目追踪文档
- [规划] 完成技术方案设计，共15个开发任务
- [决策] 确定核心技术栈：ChatGLM3-6B + LangGraph + FastAPI

---

## 资源和链接

- **完整计划**：[PLAN.md](./PLAN.md)
- **需求文档**：[cursor.md](./cursor.md)
- **代码仓库**：c:\project\agent
- **Plan文件**：c:\Users\jinghuaq\.cursor\plans\股票agent服务系统完整版_289447f1.plan.md

---

## 注意事项

1. **显存管理**：ChatGLM3-6B占4GB，bge-small-zh占500MB，需预留1-2GB给系统和并发
2. **数据准备**：50只股票数据约20MB，需提前下载避免首次使用等待
3. **知识库构建**：向量数据库需在服务启动前构建完成
4. **端口配置**：确保8765端口未被占用，防火墙已放行
5. **测试覆盖**：核心工具和Agent逻辑必须有完整测试，避免生产环境问题

---

**最后更新**：2026-01-21  
**更新人**：AI Assistant
