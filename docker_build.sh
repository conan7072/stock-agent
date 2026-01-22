#!/bin/bash
# Docker构建脚本 - 带友好提示和进度显示

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印标题
print_header() {
    echo ""
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo ""
}

# 显示菜单
show_menu() {
    print_header "🐳 股票咨询Agent - Docker构建工具"
    
    echo "请选择构建模式："
    echo ""
    echo "  1. Mock模式 (推荐测试)"
    echo "     - 无需GPU"
    echo "     - 构建快速 (~2-3分钟)"
    echo "     - 镜像小 (~500MB)"
    echo ""
    echo "  2. ChatGLM3-6B模式"
    echo "     - 需要GPU (RTX 3070 8GB+)"
    echo "     - 构建较慢 (~5-10分钟)"
    echo "     - 镜像大 (~2GB)"
    echo ""
    echo "  3. Qwen2-1.5B模式"
    echo "     - 需要GPU (RTX 3060 6GB+)"
    echo "     - 构建中等 (~4-8分钟)"
    echo "     - 镜像中等 (~1.5GB)"
    echo ""
    echo "  4. 构建所有模式"
    echo ""
    echo "  0. 退出"
    echo ""
}

# 检查Docker是否安装
check_docker() {
    print_info "检查Docker环境..."
    
    if ! command -v docker &> /dev/null; then
        print_error "未检测到Docker，请先安装Docker"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker未运行，请启动Docker"
        exit 1
    fi
    
    print_success "Docker环境正常"
}

# 检查GPU支持（仅GPU模式需要）
check_gpu() {
    print_info "检查GPU支持..."
    
    if command -v nvidia-smi &> /dev/null; then
        nvidia-smi &> /dev/null
        if [ $? -eq 0 ]; then
            print_success "检测到NVIDIA GPU"
            nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
            return 0
        fi
    fi
    
    print_warning "未检测到NVIDIA GPU"
    return 1
}

# 构建Mock模式
build_mock() {
    print_header "🔨 构建Mock模式镜像"
    
    print_info "开始构建..."
    print_info "预计时间: 2-3分钟"
    echo ""
    
    # 显示构建进度
    docker build \
        --build-arg MODE=mock \
        -t stock-agent:mock \
        --progress=plain \
        . 2>&1 | while IFS= read -r line; do
            echo "$line"
            # 提取关键步骤并高亮显示
            if [[ $line =~ "安装系统依赖" ]]; then
                print_info "步骤 1/4: 安装系统依赖"
            elif [[ $line =~ "安装Python依赖" ]]; then
                print_info "步骤 2/4: 安装Python依赖"
            elif [[ $line =~ "复制项目文件" ]]; then
                print_info "步骤 3/4: 复制项目文件"
            elif [[ $line =~ "镜像构建完成" ]]; then
                print_info "步骤 4/4: 完成配置"
            fi
        done
    
    echo ""
    print_success "Mock模式镜像构建完成！"
    print_info "镜像名称: stock-agent:mock"
    print_info "镜像大小: $(docker images stock-agent:mock --format "{{.Size}}")"
}

# 构建GPU模式
build_gpu() {
    local mode=$1
    local tag=$2
    
    print_header "🔨 构建${mode}模式镜像"
    
    # 检查GPU
    if ! check_gpu; then
        print_warning "未检测到GPU，但仍可以构建镜像"
        read -p "是否继续? [y/N]: " confirm
        if [[ ! $confirm =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    
    print_info "开始构建..."
    print_info "预计时间: 5-10分钟"
    echo ""
    
    # 显示构建进度
    docker build \
        --build-arg MODE=gpu \
        -t "stock-agent:${tag}" \
        --progress=plain \
        . 2>&1 | while IFS= read -r line; do
            echo "$line"
            # 提取关键步骤并高亮显示
            if [[ $line =~ "安装系统依赖" ]]; then
                print_info "步骤 1/4: 安装系统依赖"
            elif [[ $line =~ "安装Python依赖" ]]; then
                print_info "步骤 2/4: 安装Python依赖（包括PyTorch）"
            elif [[ $line =~ "复制项目文件" ]]; then
                print_info "步骤 3/4: 复制项目文件"
            elif [[ $line =~ "镜像构建完成" ]]; then
                print_info "步骤 4/4: 完成配置"
            fi
        done
    
    echo ""
    print_success "${mode}模式镜像构建完成！"
    print_info "镜像名称: stock-agent:${tag}"
    print_info "镜像大小: $(docker images stock-agent:${tag} --format "{{.Size}}")"
}

# 显示构建结果
show_results() {
    print_header "📊 构建结果汇总"
    
    echo "已构建的镜像："
    docker images stock-agent --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    echo ""
    print_info "下一步："
    echo "  1. 启动服务: docker-compose --profile mock up -d"
    echo "  2. 查看日志: docker-compose logs -f agent-mock"
    echo "  3. 测试接口: curl http://localhost:8765/health"
    echo ""
}

# 主函数
main() {
    # 检查Docker
    check_docker
    
    # 显示菜单
    show_menu
    
    # 读取用户选择
    read -p "请输入选项 [0-4]: " choice
    
    case $choice in
        1)
            build_mock
            show_results
            ;;
        2)
            build_gpu "ChatGLM3-6B" "chatglm3"
            show_results
            ;;
        3)
            build_gpu "Qwen2-1.5B" "qwen2"
            show_results
            ;;
        4)
            print_header "🔨 构建所有模式"
            build_mock
            echo ""
            build_gpu "ChatGLM3-6B" "chatglm3"
            echo ""
            build_gpu "Qwen2-1.5B" "qwen2"
            show_results
            ;;
        0)
            print_info "退出"
            exit 0
            ;;
        *)
            print_error "无效选项"
            exit 1
            ;;
    esac
    
    print_success "所有操作完成！"
}

# 运行主函数
main
