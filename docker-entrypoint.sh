#!/bin/bash
set -e

echo "=========================================="
echo "股票咨询Agent - Docker启动"
echo "=========================================="

# 检查是否需要下载模型
if [ "$AUTO_DOWNLOAD_MODEL" = "true" ]; then
    echo ""
    echo "📥 检查模型文件..."
    
    MODEL_PATH="${MODEL_PATH:-/app/models/chatglm3-6b}"
    
    if [ ! -d "$MODEL_PATH" ] || [ -z "$(ls -A $MODEL_PATH 2>/dev/null)" ]; then
        echo "⚠️  模型不存在，开始自动下载..."
        echo ""
        echo "模型: ${MODEL_NAME:-chatglm3-6b-int4}"
        echo "目标路径: $MODEL_PATH"
        echo ""
        
        # 在容器内下载模型
        python /app/scripts/download_model.py --model "${MODEL_NAME:-chatglm3-6b-int4}" || {
            echo "❌ 模型下载失败！"
            echo ""
            echo "可能的原因："
            echo "1. 网络问题（需要访问huggingface.co）"
            echo "2. 磁盘空间不足"
            echo ""
            echo "解决方案："
            echo "1. 设置HF镜像: export HF_ENDPOINT=https://hf-mirror.com"
            echo "2. 或手动下载模型后挂载到容器"
            exit 1
        }
        
        echo ""
        echo "✅ 模型下载完成！"
    else
        echo "✅ 模型已存在: $MODEL_PATH"
    fi
else
    echo "ℹ️  跳过模型自动下载（AUTO_DOWNLOAD_MODEL=false）"
fi

echo ""
echo "=========================================="
echo "🚀 启动Agent服务..."
echo "=========================================="
echo ""

# 启动服务
exec python /app/start_server.py
