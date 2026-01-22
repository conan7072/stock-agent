"""
测试股票工具

验证5个股票工具是否正常工作
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


def test_separator(test_name):
    """打印测试分隔符"""
    print("\n" + "=" * 60)
    print(f"[测试] {test_name}")
    print("=" * 60 + "\n")


def test_get_stock_price():
    """测试工具1：获取股票价格"""
    test_separator("工具1：获取股票价格")
    
    # 测试1：使用股票名称
    result = get_stock_price_tool.func(stock="比亚迪")
    print(result)
    
    print("\n" + "-" * 40 + "\n")
    
    # 测试2：使用股票代码
    result = get_stock_price_tool.func(stock="600519")
    print(result)


def test_get_technical_indicators():
    """测试工具2：获取技术指标"""
    test_separator("工具2：获取技术指标")
    
    result = get_technical_indicators_tool.func(stock="宁德时代")
    print(result)


def test_get_stock_history():
    """测试工具3：获取历史数据"""
    test_separator("工具3：获取历史数据")
    
    result = get_stock_history_tool.func(stock="中国平安", days=10)
    print(result)


def test_compare_stocks():
    """测试工具4：比较股票"""
    test_separator("工具4：比较股票")
    
    result = compare_stocks_tool.func(stocks=["比亚迪", "宁德时代", "贵州茅台"])
    print(result)


def test_analyze_stock():
    """测试工具5：综合分析"""
    test_separator("工具5：综合分析")
    
    result = analyze_stock_tool.func(stock="招商银行")
    print(result)


def main():
    """运行所有测试"""
    print("=" * 60)
    print("股票工具测试套件")
    print("=" * 60)
    
    tests = [
        ("获取股票价格", test_get_stock_price),
        ("获取技术指标", test_get_technical_indicators),
        ("获取历史数据", test_get_stock_history),
        ("比较股票", test_compare_stocks),
        ("综合分析", test_analyze_stock)
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
