"""
股票工具使用示例

展示如何在实际场景中使用5个股票工具
"""

import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加路径
sys.path.append(str(Path(__file__).parent))

from server.src.tools.stock_tools import (
    get_stock_price_tool,
    get_technical_indicators_tool,
    get_stock_history_tool,
    compare_stocks_tool,
    analyze_stock_tool
)


def example_1_basic_query():
    """场景1：基本查询 - 用户想知道某只股票的价格"""
    print("=" * 60)
    print("场景1：用户问'比亚迪现在多少钱？'")
    print("=" * 60)
    
    result = get_stock_price_tool.func(stock="比亚迪")
    print(result)


def example_2_technical_analysis():
    """场景2：技术分析 - 用户想了解技术面"""
    print("\n" + "=" * 60)
    print("场景2：用户问'宁德时代的技术指标怎么样？'")
    print("=" * 60)
    
    result = get_technical_indicators_tool.func(stock="宁德时代")
    print(result)


def example_3_recent_performance():
    """场景3：近期表现 - 用户想看最近走势"""
    print("\n" + "=" * 60)
    print("场景3：用户问'贵州茅台最近表现如何？'")
    print("=" * 60)
    
    result = get_stock_history_tool.func(stock="贵州茅台", days=5)
    print(result)


def example_4_stock_comparison():
    """场景4：对比分析 - 用户想比较多只股票"""
    print("\n" + "=" * 60)
    print("场景4：用户问'比较一下新能源汽车板块的主要股票'")
    print("=" * 60)
    
    result = compare_stocks_tool.func(
        stocks=["比亚迪", "宁德时代", "理想汽车"]
    )
    print(result)


def example_5_comprehensive_analysis():
    """场景5：综合分析 - 用户想全面了解一只股票"""
    print("\n" + "=" * 60)
    print("场景5：用户问'给我全面分析一下中国平安'")
    print("=" * 60)
    
    result = analyze_stock_tool.func(stock="中国平安")
    print(result)


def example_6_multi_step_reasoning():
    """场景6：多步推理 - Agent需要调用多个工具"""
    print("\n" + "=" * 60)
    print("场景6：用户问'银行股中哪个技术面比较好？'")
    print("=" * 60)
    print("\nAgent的推理过程：")
    print("1. 首先对比几只银行股")
    print("2. 再查看技术指标最好的那只\n")
    
    # 步骤1：对比银行股
    print("[步骤1] 对比银行股：")
    print("-" * 40)
    compare_result = compare_stocks_tool.func(
        stocks=["招商银行", "工商银行", "建设银行"]
    )
    print(compare_result)
    
    # 步骤2：查看表现最好的技术指标（假设是招商银行）
    print("\n[步骤2] 查看招商银行的技术指标：")
    print("-" * 40)
    tech_result = get_technical_indicators_tool.func(stock="招商银行")
    print(tech_result)
    
    print("\n[Agent总结]")
    print("根据对比分析和技术指标，招商银行...")


def example_7_investment_advice():
    """场景7：投资建议 - 综合多个工具给出建议"""
    print("\n" + "=" * 60)
    print("场景7：用户问'比亚迪值得投资吗？'")
    print("=" * 60)
    print("\nAgent的分析流程：")
    print("1. 查看最新价格")
    print("2. 分析技术指标")
    print("3. 查看近期走势")
    print("4. 综合给出建议\n")
    
    # 步骤1：最新价格
    print("[步骤1] 最新价格：")
    print("-" * 40)
    price_result = get_stock_price_tool.func(stock="比亚迪")
    print(price_result)
    
    # 步骤2：技术指标
    print("\n[步骤2] 技术指标：")
    print("-" * 40)
    tech_result = get_technical_indicators_tool.func(stock="比亚迪")
    print(tech_result)
    
    # 步骤3：近期走势
    print("\n[步骤3] 近期走势：")
    print("-" * 40)
    history_result = get_stock_history_tool.func(stock="比亚迪", days=5)
    print(history_result)
    
    print("\n[Agent建议]")
    print("综合以上分析...")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("股票工具使用示例集")
    print("=" * 60 + "\n")
    
    examples = [
        ("基本查询", example_1_basic_query),
        ("技术分析", example_2_technical_analysis),
        ("近期表现", example_3_recent_performance),
        ("对比分析", example_4_stock_comparison),
        ("综合分析", example_5_comprehensive_analysis),
        ("多步推理", example_6_multi_step_reasoning),
        ("投资建议", example_7_investment_advice)
    ]
    
    print("请选择要运行的示例：")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  {len(examples)+1}. 运行所有示例")
    
    choice = input("\n请输入选项（1-8）：").strip()
    
    if choice == str(len(examples) + 1):
        # 运行所有示例
        for name, func in examples:
            func()
            input("\n按Enter继续...")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        # 运行指定示例
        examples[int(choice) - 1][1]()
    else:
        print("无效的选项")


if __name__ == "__main__":
    # 默认运行前3个简单示例
    example_1_basic_query()
    example_2_technical_analysis()
    example_3_recent_performance()
    
    print("\n" + "=" * 60)
    print("更多示例请运行：python example_tool_usage.py")
    print("=" * 60)
