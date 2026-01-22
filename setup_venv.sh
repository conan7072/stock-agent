#!/bin/bash
# Bash脚本：创建和配置虚拟环境 (Linux/Mac)

echo "======================================"
echo "  股票Agent系统 - 环境设置"
echo "======================================"
echo ""

# 检查Python版本
echo "🔍 检查Python版本..."
python_version=$(python3 --version 2>&1)
echo "   $python_version"

if [[ $python_version =~ Python\ 3\.([0-9]+)\. ]]; then
    minor_version=${BASH_REMATCH[1]}
    if [ "$minor_version" -lt 10 ]; then
        echo "   ❌ Python版本过低，需要 >= 3.10"
        exit 1
    fi
    echo "   ✅ Python版本符合要求"
fi

echo ""

# 创建虚拟环境
if [ -d "venv" ]; then
    echo "📦 虚拟环境已存在"
    read -p "是否重新创建? [y/N]: " recreate
    if [ "$recreate" = "y" ] || [ "$recreate" = "Y" ]; then
        echo "   删除旧环境..."
        rm -rf venv
    else
        echo "   跳过创建"
        echo ""
        echo "🚀 激活虚拟环境:"
        echo "   source venv/bin/activate"
        exit 0
    fi
fi

echo "📦 创建虚拟环境..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "   ❌ 创建失败"
    exit 1
fi

echo "   ✅ 创建成功"
echo ""

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "📦 升级pip..."
python -m pip install --upgrade pip -q

echo "   ✅ pip已升级"
echo ""

# 询问是否安装依赖
echo "📦 是否安装项目依赖?"
echo "   1. 服务端依赖 (需要GPU)"
echo "   2. 客户端依赖 (无需GPU)"
echo "   3. 全部依赖"
echo "   4. 跳过"

read -p "请选择 [1-4]: " choice

case $choice in
    1)
        echo "   安装服务端依赖..."
        pip install -r server/requirements.txt
        ;;
    2)
        echo "   安装客户端依赖..."
        pip install -r client/requirements.txt
        ;;
    3)
        echo "   安装全部依赖..."
        pip install -r requirements.txt
        ;;
    *)
        echo "   跳过安装依赖"
        ;;
esac

echo ""
echo "======================================"
echo "  ✅ 环境设置完成！"
echo "======================================"
echo ""
echo "🚀 下一步操作:"
echo ""
echo "1. 激活虚拟环境 (如果未激活):"
echo "   source venv/bin/activate"
echo ""
echo "2. 运行环境检查:"
echo "   python scripts/setup_env.py"
echo ""
echo "3. 下载模型:"
echo "   python scripts/download_model.py"
echo ""
echo "4. 下载数据:"
echo "   python scripts/download_stock_data.py"
echo ""
