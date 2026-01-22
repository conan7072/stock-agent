"""
测试Stock Agent

验证Agent是否能正确处理各种查询
"""

import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加路径
sys.path.append(str(Path(__file__).parent))

from server.src.agent.stock_agent import get_agent


def test_separator(test_name):
    """打印测试分隔符"""
    print("\n" + "=" * 70)
    print(f"[测试] {test_name}")
    print("=" * 70 + "\n")


def test_price_query():
    """测试价格查询"""
    test_separator("价格查询")
    
    agent = get_agent()
    
    queries = [
        "比亚迪现在多少钱？",
        "宁德时代的股价是多少？"
    ]
    
    for query in queries:
        print(f"用户: {query}")
        print("-" * 70)
        
        answer = agent.query(query)
        print(f"Agent: {answer}")
        print()


def test_technical_query():
    """测试技术指标查询"""
    test_separator("技术指标查询")
    
    agent = get_agent()
    
    queries = [
        "贵州茅台的技术指标怎么样？",
        "分析一下中国平安"
    ]
    
    for query in queries:
        print(f"用户: {query}")
        print("-" * 70)
        
        answer = agent.query(query)
        print(f"Agent: {answer}")
        print()


def test_knowledge_query():
    """测试知识查询"""
    test_separator("知识查询")
    
    agent = get_agent()
    
    queries = [
        "什么是MACD指标？",
        "如何看均线？"
    ]
    
    for query in queries:
        print(f"用户: {query}")
        print("-" * 70)
        
        answer = agent.query(query)
        print(f"Agent: {answer}")
        print()


def test_comparison_query():
    """测试对比查询"""
    test_separator("对比查询")
    
    agent = get_agent()
    
    queries = [
        "对比一下比亚迪和宁德时代",
    ]
    
    for query in queries:
        print(f"用户: {query}")
        print("-" * 70)
        
        answer = agent.query(query)
        print(f"Agent: {answer}")
        print()


def test_history_query():
    """测试历史查询"""
    test_separator("历史查询")
    
    agent = get_agent()
    
    queries = [
        "招商银行最近5天的表现如何？",
    ]
    
    for query in queries:
        print(f"用户: {query}")
        print("-" * 70)
        
        answer = agent.query(query)
        print(f"Agent: {answer}")
        print()


def interactive_mode():
    """交互模式"""
    test_separator("交互模式")
    
    agent = get_agent()
    
    print("股票咨询Agent - 交互模式")
    print("输入 'exit' 或 'quit' 退出")
    print("-" * 70)
    
    while True:
        try:
            user_input = input("\n用户: ").strip()
            
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("\n再见!")
                break
            
            if not user_input:
                continue
            
            print()
            answer = agent.query(user_input)
            print(f"Agent: {answer}")
            
        except KeyboardInterrupt:
            print("\n\n再见!")
            break
        except Exception as e:
            print(f"\n错误: {str(e)}")


def main():
    """运行测试"""
    print("=" * 70)
    print("股票Agent测试套件")
    print("=" * 70)
    
    # 自动测试
    tests = [
        ("价格查询", test_price_query),
        ("技术指标查询", test_technical_query),
        ("知识查询", test_knowledge_query),
        ("对比查询", test_comparison_query),
        ("历史查询", test_history_query)
    ]
    
    print("\n[模式选择]")
    print("1. 运行自动测试")
    print("2. 进入交互模式")
    print("3. 运行所有测试后进入交互模式")
    
    choice = input("\n请选择 (默认1): ").strip()
    
    if choice == "2":
        interactive_mode()
    elif choice == "3":
        for i, (name, test_func) in enumerate(tests, 1):
            try:
                test_func()
                print(f"[OK] 测试 {i}/{len(tests)} 完成: {name}")
            except Exception as e:
                print(f"[ERROR] 测试 {i}/{len(tests)} 失败: {name}")
                print(f"错误: {str(e)}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "=" * 70)
        print("自动测试完成，现在进入交互模式...")
        print("=" * 70)
        
        interactive_mode()
    else:
        # 默认运行自动测试
        for i, (name, test_func) in enumerate(tests, 1):
            try:
                test_func()
                print(f"[OK] 测试 {i}/{len(tests)} 完成: {name}")
            except Exception as e:
                print(f"[ERROR] 测试 {i}/{len(tests)} 失败: {name}")
                print(f"错误: {str(e)}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "=" * 70)
        print("测试完成！")
        print("=" * 70)


if __name__ == "__main__":
    main()
