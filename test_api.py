"""
测试API接口

使用requests库测试FastAPI服务
"""

import sys
from pathlib import Path
import requests
import json

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


API_BASE = "http://localhost:8765"


def test_separator(test_name):
    """打印测试分隔符"""
    print("\n" + "=" * 70)
    print(f"[测试] {test_name}")
    print("=" * 70 + "\n")


def test_health_check():
    """测试健康检查"""
    test_separator("健康检查")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"状态: {data.get('status')}")
            print(f"Agent就绪: {data.get('agent_ready')}")
            return True
        else:
            print(f"错误: HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"连接失败: {str(e)}")
        print("\n请确保服务器已启动:")
        print("  python start_server.py")
        return False


def test_chat():
    """测试聊天接口"""
    test_separator("聊天接口")
    
    queries = [
        "比亚迪现在多少钱？",
        "什么是MACD指标？"
    ]
    
    for query in queries:
        print(f"用户: {query}")
        print("-" * 70)
        
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    answer = data.get('answer', '')
                    print(f"Agent: {answer[:200]}...")
                else:
                    print(f"错误: {data.get('error')}")
            else:
                print(f"HTTP错误: {response.status_code}")
        
        except Exception as e:
            print(f"请求失败: {str(e)}")
        
        print()


def test_list_tools():
    """测试工具列表"""
    test_separator("工具列表")
    
    try:
        response = requests.get(f"{API_BASE}/tools", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            tools = data.get('tools', [])
            
            print(f"共 {len(tools)} 个工具:\n")
            
            for i, tool in enumerate(tools, 1):
                print(f"{i}. {tool['name']}")
                print(f"   {tool['description'][:80]}...")
                print()
        else:
            print(f"HTTP错误: {response.status_code}")
    
    except Exception as e:
        print(f"请求失败: {str(e)}")


def test_list_stocks():
    """测试股票列表"""
    test_separator("股票列表")
    
    try:
        response = requests.get(f"{API_BASE}/stocks", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            stocks = data.get('stocks', [])
            
            print(f"共 {len(stocks)} 只股票\n")
            print("前10只:")
            
            for i, stock in enumerate(stocks[:10], 1):
                print(f"  {i}. {stock['name']} ({stock['code']})")
        else:
            print(f"HTTP错误: {response.status_code}")
    
    except Exception as e:
        print(f"请求失败: {str(e)}")


def main():
    """运行所有测试"""
    print("=" * 70)
    print("API测试套件")
    print("=" * 70)
    
    # 首先检查服务器是否运行
    if not test_health_check():
        return
    
    # 运行其他测试
    tests = [
        ("工具列表", test_list_tools),
        ("股票列表", test_list_stocks),
        ("聊天接口", test_chat)
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"[OK] {name} 测试完成")
        except Exception as e:
            print(f"[ERROR] {name} 测试失败: {str(e)}")
    
    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()
