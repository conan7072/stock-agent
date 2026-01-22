#!/bin/bash
# Docker测试脚本 - 启动并测试服务

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo ""
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo ""
}

# 启动服务
start_service() {
    print_header "🚀 启动Mock模式服务"
    
    print_info "停止已有容器..."
    docker-compose --profile mock down 2>/dev/null || true
    
    print_info "启动新容器..."
    docker-compose --profile mock up -d
    
    print_info "等待服务启动..."
    sleep 5
    
    print_success "服务已启动"
}

# 测试健康检查
test_health() {
    print_header "🏥 健康检查测试"
    
    print_info "测试 /health 端点..."
    response=$(curl -s http://localhost:8765/health)
    
    if echo "$response" | grep -q "healthy"; then
        print_success "健康检查通过"
        echo "$response" | jq '.' 2>/dev/null || echo "$response"
    else
        print_warning "健康检查失败"
        echo "$response"
        return 1
    fi
}

# 测试聊天接口
test_chat() {
    print_header "💬 聊天接口测试"
    
    print_info "发送测试查询: '比亚迪现在多少钱？'"
    response=$(curl -s -X POST http://localhost:8765/chat \
        -H "Content-Type: application/json" \
        -d '{"query": "比亚迪现在多少钱？"}')
    
    if echo "$response" | grep -q "success"; then
        print_success "聊天接口正常"
        echo "$response" | jq '.answer' 2>/dev/null | head -c 200
        echo "..."
    else
        print_warning "聊天接口异常"
        echo "$response"
        return 1
    fi
}

# 测试工具列表
test_tools() {
    print_header "🔧 工具列表测试"
    
    print_info "获取工具列表..."
    response=$(curl -s http://localhost:8765/tools)
    
    count=$(echo "$response" | jq '.count' 2>/dev/null)
    if [ "$count" == "5" ]; then
        print_success "工具列表正常 ($count 个工具)"
        echo "$response" | jq '.tools[].name' 2>/dev/null
    else
        print_warning "工具列表异常"
        echo "$response"
        return 1
    fi
}

# 测试股票列表
test_stocks() {
    print_header "📊 股票列表测试"
    
    print_info "获取股票列表..."
    response=$(curl -s http://localhost:8765/stocks)
    
    count=$(echo "$response" | jq '.count' 2>/dev/null)
    if [ "$count" -gt "0" ]; then
        print_success "股票列表正常 ($count 只股票)"
        echo "$response" | jq '.stocks[:5]' 2>/dev/null
        echo "..."
    else
        print_warning "股票列表异常"
        echo "$response"
        return 1
    fi
}

# 显示日志
show_logs() {
    print_header "📋 查看容器日志"
    
    print_info "最近20行日志:"
    docker-compose logs --tail=20 agent-mock
}

# 交互式测试
interactive_test() {
    print_header "🎮 交互式测试"
    
    echo "输入你的问题（输入 'exit' 退出）："
    echo ""
    
    while true; do
        read -p "您: " query
        
        if [ "$query" == "exit" ]; then
            break
        fi
        
        if [ -z "$query" ]; then
            continue
        fi
        
        echo ""
        echo "Agent: 思考中..."
        
        response=$(curl -s -X POST http://localhost:8765/chat \
            -H "Content-Type: application/json" \
            -d "{\"query\": \"$query\"}")
        
        answer=$(echo "$response" | jq -r '.answer' 2>/dev/null)
        
        if [ -n "$answer" ] && [ "$answer" != "null" ]; then
            echo "$answer"
        else
            echo "错误: $response"
        fi
        
        echo ""
        echo "------------------------------------------------------------"
        echo ""
    done
}

# 性能测试
performance_test() {
    print_header "⚡ 性能测试"
    
    print_info "测试响应时间（10次请求）..."
    
    total_time=0
    success_count=0
    
    for i in {1..10}; do
        start=$(date +%s%N)
        response=$(curl -s -X POST http://localhost:8765/chat \
            -H "Content-Type: application/json" \
            -d '{"query": "测试"}')
        end=$(date +%s%N)
        
        duration=$((($end - $start) / 1000000))
        
        if echo "$response" | grep -q "success"; then
            ((success_count++))
            total_time=$(($total_time + $duration))
            echo "  请求 $i: ${duration}ms ✓"
        else
            echo "  请求 $i: 失败 ✗"
        fi
    done
    
    if [ $success_count -gt 0 ]; then
        avg_time=$(($total_time / $success_count))
        print_success "平均响应时间: ${avg_time}ms"
        print_success "成功率: $(($success_count * 10))%"
    fi
}

# 主菜单
show_menu() {
    echo ""
    echo "============================================================"
    echo "🧪 Docker测试菜单"
    echo "============================================================"
    echo ""
    echo "  1. 启动服务"
    echo "  2. 运行所有测试"
    echo "  3. 健康检查"
    echo "  4. 聊天接口测试"
    echo "  5. 工具和股票列表"
    echo "  6. 查看日志"
    echo "  7. 交互式测试"
    echo "  8. 性能测试"
    echo "  9. 停止服务"
    echo "  0. 退出"
    echo ""
}

# 主函数
main() {
    while true; do
        show_menu
        read -p "请选择 [0-9]: " choice
        
        case $choice in
            1)
                start_service
                ;;
            2)
                test_health && \
                test_chat && \
                test_tools && \
                test_stocks && \
                print_success "所有测试通过！"
                ;;
            3)
                test_health
                ;;
            4)
                test_chat
                ;;
            5)
                test_tools
                test_stocks
                ;;
            6)
                show_logs
                ;;
            7)
                interactive_test
                ;;
            8)
                performance_test
                ;;
            9)
                print_info "停止服务..."
                docker-compose --profile mock down
                print_success "服务已停止"
                ;;
            0)
                print_info "退出"
                exit 0
                ;;
            *)
                print_warning "无效选项"
                ;;
        esac
        
        read -p "按Enter继续..."
    done
}

# 检查依赖
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        print_warning "未安装Docker"
        exit 1
    fi
    
    if ! command -v curl &> /dev/null; then
        print_warning "未安装curl"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        print_warning "未安装jq（可选，用于格式化JSON）"
    fi
}

# 运行
check_dependencies
main
