# 股票咨询Agent - 多模式支持
# 支持：Mock模式（无GPU）、ChatGLM3-6B、Qwen2-1.5B
# 
# 构建示例：
#   docker build --build-arg MODE=mock -t stock-agent:mock .
#   docker build --build-arg MODE=chatglm3 -t stock-agent:chatglm3 .
#   docker build --build-arg MODE=qwen2 -t stock-agent:qwen2 .

# 第一阶段：选择基础镜像
ARG MODE=mock
FROM python:3.11-slim as base-mock
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04 as base-gpu

# 第二阶段：根据模式选择基础镜像
FROM base-${MODE} as base
ARG MODE=mock

# 安装基础工具
RUN echo "============================================================" && \
    echo "📦 安装系统依赖..." && \
    echo "============================================================" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        git \
        && rm -rf /var/lib/apt/lists/* && \
    echo "✅ 系统依赖安装完成"

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .
COPY server/requirements.txt ./server/

# 安装Python依赖
RUN echo "============================================================" && \
    echo "📚 安装Python依赖 (MODE=${MODE})..." && \
    echo "============================================================" && \
    if [ "${MODE}" = "mock" ]; then \
        echo "  → Mock模式：安装轻量级依赖" && \
        pip install --no-cache-dir \
            fastapi==0.109.0 \
            uvicorn==0.27.0 \
            pydantic==2.12.5 \
            pyyaml==6.0.3 \
            pandas==2.2.0 \
            pyarrow==15.0.0 \
            requests==2.32.5 \
            langchain==1.2.6 \
            langchain-core==1.2.7 \
            -i https://pypi.tuna.tsinghua.edu.cn/simple && \
        echo "✅ Mock模式依赖安装完成"; \
    else \
        echo "  → GPU模式：安装完整依赖（包括PyTorch）" && \
        pip install --no-cache-dir \
            torch==2.1.0 \
            transformers==4.36.0 \
            accelerate==0.25.0 \
            -i https://pypi.tuna.tsinghua.edu.cn/simple && \
        pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
        echo "✅ GPU模式依赖安装完成"; \
    fi

# 复制项目文件
RUN echo "============================================================" && \
    echo "📁 复制项目文件..." && \
    echo "============================================================"

COPY server/ ./server/
COPY client/ ./client/
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY start_server.py .
COPY start_client.py .

RUN echo "✅ 项目文件复制完成"

# 创建必要的目录
RUN mkdir -p models logs && \
    echo "✅ 目录结构创建完成"

# 暴露端口
EXPOSE 8765

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV MODE=${MODE}

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8765/health || exit 1

# 启动脚本
RUN echo "============================================================" && \
    echo "🎉 镜像构建完成！" && \
    echo "============================================================" && \
    echo "模式: ${MODE}" && \
    echo "端口: 8765" && \
    echo "============================================================"

# 复制启动脚本
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# 启动命令
ENTRYPOINT ["/app/docker-entrypoint.sh"]
