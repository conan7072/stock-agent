"""
测试RAG系统

验证知识库检索是否正常工作
"""

import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加路径
sys.path.append(str(Path(__file__).parent))

from server.src.rag.simple_retriever import get_retriever


def test_separator(test_name):
    """打印测试分隔符"""
    print("\n" + "=" * 60)
    print(f"[测试] {test_name}")
    print("=" * 60 + "\n")


def test_basic_search():
    """测试基本搜索"""
    test_separator("基本搜索")
    
    retriever = get_retriever()
    
    queries = [
        "什么是市盈率？",
        "如何看MACD指标？",
        "股票涨跌停是什么意思？"
    ]
    
    for query in queries:
        print(f"查询：{query}")
        print("-" * 40)
        
        results = retriever.search(query, top_k=2)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"\n结果 {i} (得分: {result['score']:.2f})")
                print(f"标题: {result.get('title', '无')}")
                print(f"内容: {result['content'][:150]}...")
        else:
            print("未找到相关知识")
        
        print("\n" + "=" * 60)


def test_knowledge_detection():
    """测试知识查询检测"""
    test_separator("知识查询检测")
    
    retriever = get_retriever()
    
    test_cases = [
        ("什么是市盈率？", True),
        ("比亚迪现在多少钱？", False),
        ("如何分析技术指标？", True),
        ("宁德时代怎么样？", False),
        ("解释一下MACD", True)
    ]
    
    for query, expected in test_cases:
        is_knowledge = retriever.is_knowledge_query(query)
        status = "OK" if is_knowledge == expected else "FAIL"
        print(f"[{status}] '{query}' -> {is_knowledge} (预期: {expected})")


def test_context_generation():
    """测试上下文生成"""
    test_separator("上下文生成")
    
    retriever = get_retriever()
    
    query = "什么是技术分析？"
    
    print(f"查询：{query}")
    print("-" * 40)
    
    context = retriever.get_context(query, max_length=300)
    
    if context:
        print(f"生成的上下文：\n{context}")
        print(f"\n长度：{len(context)}字符")
    else:
        print("未生成上下文")


def test_relevant_knowledge():
    """测试相关知识获取"""
    test_separator("相关知识获取")
    
    retriever = get_retriever()
    
    queries = [
        "什么是MACD？",
        "比亚迪的价格",
        "如何看均线？",
        "宁德时代分析"
    ]
    
    for query in queries:
        print(f"查询：{query}")
        print("-" * 40)
        
        knowledge = retriever.get_relevant_knowledge(query)
        
        if knowledge:
            print(f"找到相关知识：\n{knowledge[:200]}...")
        else:
            print("无需知识库（或未找到）")
        
        print("\n")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("RAG系统测试套件")
    print("=" * 60)
    
    tests = [
        ("基本搜索", test_basic_search),
        ("知识查询检测", test_knowledge_detection),
        ("上下文生成", test_context_generation),
        ("相关知识获取", test_relevant_knowledge)
    ]
    
    for i, (name, test_func) in enumerate(tests, 1):
        try:
            test_func()
            print(f"\n[OK] 测试 {i}/{len(tests)} 通过: {name}")
        except Exception as e:
            print(f"\n[ERROR] 测试 {i}/{len(tests)} 失败: {name}")
            print(f"错误信息: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
