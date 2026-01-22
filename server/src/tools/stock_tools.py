"""
股票工具集

实现5个核心股票查询工具，供Agent使用
"""

from typing import Optional, List, Dict, Any, Callable
from pydantic import BaseModel, Field
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from server.src.data.stock_loader import get_loader
from server.src.data.stock_analyzer import (
    calculate_ma,
    calculate_macd,
    calculate_rsi,
    calculate_boll,
    analyze_trend,
    get_support_resistance,
    calculate_volume_ratio
)


# ==================== 简化的工具类 ====================

class SimpleTool:
    """简化的工具类，用于无GPU版本"""
    
    def __init__(
        self,
        name: str,
        description: str,
        func: Callable,
        args_schema: type[BaseModel]
    ):
        self.name = name
        self.description = description
        self.func = func
        self.args_schema = args_schema
    
    def run(self, **kwargs) -> str:
        """运行工具"""
        return self.func(**kwargs)
    
    def __call__(self, **kwargs) -> str:
        """使工具可调用"""
        return self.run(**kwargs)


# ==================== 工具1：获取股票价格 ====================

class GetStockPriceInput(BaseModel):
    """获取股票价格的输入参数"""
    stock: str = Field(description="股票名称或代码，如'比亚迪'或'002594'")


def get_stock_price_func(stock: str) -> str:
    """
    获取指定股票的最新价格信息
    
    Args:
        stock: 股票名称或代码
        
    Returns:
        价格信息的字符串描述
    """
    try:
        loader = get_loader()
        price_info = loader.get_latest_price(stock)
        
        if price_info is None:
            return f"未找到股票 '{stock}' 的数据。请检查股票名称或代码是否正确。"
        
        result = f"【{stock}】最新行情：\n"
        result += f"日期：{price_info['date']}\n"
        result += f"收盘价：{price_info['close']:.2f}元\n"
        result += f"开盘价：{price_info['open']:.2f}元\n"
        result += f"最高价：{price_info['high']:.2f}元\n"
        result += f"最低价：{price_info['low']:.2f}元\n"
        result += f"成交量：{price_info['volume']:,}手\n"
        
        if price_info.get('change_pct') is not None:
            change_pct = price_info['change_pct']
            result += f"涨跌幅：{change_pct:+.2f}%\n"
        
        return result
    
    except Exception as e:
        return f"获取股票价格失败：{str(e)}"


get_stock_price_tool = SimpleTool(
    name="get_stock_price",
    description="获取指定股票的最新价格、成交量等行情信息。适合回答'XX股票现在多少钱'、'XX股票价格'等问题。",
    func=get_stock_price_func,
    args_schema=GetStockPriceInput
)


# ==================== 工具2：获取技术指标 ====================

class GetTechnicalIndicatorsInput(BaseModel):
    """获取技术指标的输入参数"""
    stock: str = Field(description="股票名称或代码，如'比亚迪'或'002594'")


def get_technical_indicators_func(stock: str) -> str:
    """
    获取指定股票的技术指标（MA、MACD、RSI、BOLL等）
    
    Args:
        stock: 股票名称或代码
        
    Returns:
        技术指标信息的字符串描述
    """
    try:
        loader = get_loader()
        df = loader.get_stock_data(stock)
        
        if df is None or len(df) == 0:
            return f"未找到股票 '{stock}' 的数据。"
        
        result = f"【{stock}】技术指标分析：\n\n"
        
        # MA均线
        ma = calculate_ma(df)
        if ma:
            result += "【移动平均线】\n"
            for key, value in ma.items():
                result += f"  {key}: {value:.2f}元\n"
            result += "\n"
        
        # MACD
        macd = calculate_macd(df)
        if macd:
            result += "【MACD指标】\n"
            result += f"  DIF: {macd['DIF']:.2f}\n"
            result += f"  DEA: {macd['DEA']:.2f}\n"
            result += f"  MACD: {macd['MACD']:.2f}\n"
            result += f"  信号: {macd['signal']}\n\n"
        
        # RSI
        rsi = calculate_rsi(df)
        if rsi:
            result += "【RSI指标】\n"
            result += f"  RSI(14): {rsi:.2f}\n"
            if rsi > 70:
                result += "  状态: 超买区域，注意回调风险\n"
            elif rsi < 30:
                result += "  状态: 超卖区域，可能存在反弹机会\n"
            else:
                result += "  状态: 正常区域\n"
            result += "\n"
        
        # 布林带
        boll = calculate_boll(df)
        if boll:
            result += "【布林带】\n"
            result += f"  上轨: {boll['upper']:.2f}元\n"
            result += f"  中轨: {boll['middle']:.2f}元\n"
            result += f"  下轨: {boll['lower']:.2f}元\n"
            result += f"  当前价格: {boll['current']:.2f}元 ({boll['position']})\n\n"
        
        # 趋势分析
        trend = analyze_trend(df)
        result += f"【趋势判断】{trend}\n\n"
        
        # 支撑压力
        sr = get_support_resistance(df)
        if sr:
            result += "【支撑/压力位】\n"
            result += f"  支撑位: {sr['support']:.2f}元\n"
            result += f"  压力位: {sr['resistance']:.2f}元\n\n"
        
        # 量比
        volume_ratio = calculate_volume_ratio(df)
        if volume_ratio:
            result += f"【量比】{volume_ratio:.2f}\n"
            if volume_ratio > 2:
                result += "  成交量显著放大\n"
            elif volume_ratio < 0.5:
                result += "  成交量萎缩\n"
        
        return result
    
    except Exception as e:
        return f"获取技术指标失败：{str(e)}"


get_technical_indicators_tool = SimpleTool(
    name="get_technical_indicators",
    description="获取指定股票的技术指标，包括MA均线、MACD、RSI、布林带、趋势判断等。适合回答'XX技术面分析'、'XX技术指标如何'等问题。",
    func=get_technical_indicators_func,
    args_schema=GetTechnicalIndicatorsInput
)


# ==================== 工具3：获取历史数据 ====================

class GetStockHistoryInput(BaseModel):
    """获取历史数据的输入参数"""
    stock: str = Field(description="股票名称或代码，如'比亚迪'或'002594'")
    days: int = Field(default=10, description="获取最近N天的数据，默认10天")


def get_stock_history_func(stock: str, days: int = 10) -> str:
    """
    获取指定股票的历史数据
    
    Args:
        stock: 股票名称或代码
        days: 获取最近N天的数据
        
    Returns:
        历史数据的字符串描述
    """
    try:
        loader = get_loader()
        df = loader.get_stock_data(stock)
        
        if df is None or len(df) == 0:
            return f"未找到股票 '{stock}' 的数据。"
        
        # 限制天数
        days = min(days, 30)  # 最多返回30天
        days = max(days, 1)   # 至少返回1天
        
        recent_df = df.tail(days)
        
        result = f"【{stock}】最近{len(recent_df)}个交易日数据：\n\n"
        result += f"{'日期':<12} {'收盘':<8} {'涨跌幅':<8} {'成交量':<12}\n"
        result += "-" * 50 + "\n"
        
        for _, row in recent_df.iterrows():
            date_str = str(row['date'])[:10]
            close = row['close']
            change_pct = row.get('change_pct', 0)
            volume = row['volume']
            
            result += f"{date_str:<12} {close:>7.2f} {change_pct:>6.2f}% {volume:>10,}手\n"
        
        # 统计信息
        result += "\n【统计信息】\n"
        result += f"  最高价: {recent_df['high'].max():.2f}元\n"
        result += f"  最低价: {recent_df['low'].min():.2f}元\n"
        result += f"  平均价: {recent_df['close'].mean():.2f}元\n"
        
        change_total = ((recent_df.iloc[-1]['close'] - recent_df.iloc[0]['close']) / recent_df.iloc[0]['close']) * 100
        result += f"  区间涨跌: {change_total:+.2f}%\n"
        
        return result
    
    except Exception as e:
        return f"获取历史数据失败：{str(e)}"


get_stock_history_tool = SimpleTool(
    name="get_stock_history",
    description="获取指定股票最近N天的历史交易数据。适合回答'XX最近表现如何'、'XX近期走势'等问题。",
    func=get_stock_history_func,
    args_schema=GetStockHistoryInput
)


# ==================== 工具4：比较股票 ====================

class CompareStocksInput(BaseModel):
    """比较股票的输入参数"""
    stocks: List[str] = Field(description="要比较的股票列表，如['比亚迪', '宁德时代']")


def compare_stocks_func(stocks: List[str]) -> str:
    """
    比较多只股票的表现
    
    Args:
        stocks: 股票列表
        
    Returns:
        对比结果的字符串描述
    """
    try:
        if len(stocks) < 2:
            return "请至少提供2只股票进行对比。"
        
        if len(stocks) > 5:
            return "最多支持同时比较5只股票。"
        
        loader = get_loader()
        
        result = f"【股票对比】共{len(stocks)}只\n\n"
        result += f"{'股票':<10} {'最新价':<10} {'今日涨跌':<10} {'5日涨跌':<10} {'20日涨跌':<10}\n"
        result += "-" * 60 + "\n"
        
        stock_data = []
        
        for stock in stocks:
            df = loader.get_stock_data(stock)
            if df is None or len(df) == 0:
                result += f"{stock:<10} 数据缺失\n"
                continue
            
            latest = df.iloc[-1]
            latest_price = latest['close']
            today_change = latest.get('change_pct', 0)
            
            # 5日涨跌
            if len(df) >= 5:
                change_5d = ((df.tail(5).iloc[-1]['close'] - df.tail(5).iloc[0]['close']) / df.tail(5).iloc[0]['close']) * 100
            else:
                change_5d = 0
            
            # 20日涨跌
            if len(df) >= 20:
                change_20d = ((df.tail(20).iloc[-1]['close'] - df.tail(20).iloc[0]['close']) / df.tail(20).iloc[0]['close']) * 100
            else:
                change_20d = 0
            
            result += f"{stock:<10} {latest_price:>8.2f} {today_change:>8.2f}% {change_5d:>8.2f}% {change_20d:>8.2f}%\n"
            
            stock_data.append({
                'name': stock,
                'price': latest_price,
                'today': today_change,
                '5d': change_5d,
                '20d': change_20d
            })
        
        # 分析
        if len(stock_data) >= 2:
            result += "\n【对比分析】\n"
            
            # 今日最强
            best_today = max(stock_data, key=lambda x: x['today'])
            result += f"  今日涨幅最大: {best_today['name']} ({best_today['today']:+.2f}%)\n"
            
            # 5日最强
            best_5d = max(stock_data, key=lambda x: x['5d'])
            result += f"  5日涨幅最大: {best_5d['name']} ({best_5d['5d']:+.2f}%)\n"
            
            # 20日最强
            best_20d = max(stock_data, key=lambda x: x['20d'])
            result += f"  20日涨幅最大: {best_20d['name']} ({best_20d['20d']:+.2f}%)\n"
        
        return result
    
    except Exception as e:
        return f"比较股票失败：{str(e)}"


compare_stocks_tool = SimpleTool(
    name="compare_stocks",
    description="比较多只股票的表现，包括最新价格、今日涨跌、近期涨跌等。适合回答'比较XX和YY'、'XX和YY哪个好'等问题。",
    func=compare_stocks_func,
    args_schema=CompareStocksInput
)


# ==================== 工具5：综合分析股票 ====================

class AnalyzeStockInput(BaseModel):
    """综合分析股票的输入参数"""
    stock: str = Field(description="股票名称或代码，如'比亚迪'或'002594'")


def analyze_stock_func(stock: str) -> str:
    """
    对股票进行综合分析（价格+技术指标+趋势）
    
    Args:
        stock: 股票名称或代码
        
    Returns:
        综合分析结果
    """
    try:
        loader = get_loader()
        df = loader.get_stock_data(stock)
        
        if df is None or len(df) == 0:
            return f"未找到股票 '{stock}' 的数据。"
        
        result = f"【{stock}】综合分析报告\n"
        result += "=" * 50 + "\n\n"
        
        # 1. 基本信息
        latest = df.iloc[-1]
        result += "【基本行情】\n"
        result += f"  日期: {latest['date']}\n"
        result += f"  收盘价: {latest['close']:.2f}元\n"
        result += f"  涨跌幅: {latest.get('change_pct', 0):+.2f}%\n"
        result += f"  成交量: {latest['volume']:,}手\n"
        result += f"  数据记录: {len(df)}条\n\n"
        
        # 2. 近期表现
        result += "【近期表现】\n"
        for days in [5, 20, 60]:
            if len(df) >= days:
                change = ((df.tail(days).iloc[-1]['close'] - df.tail(days).iloc[0]['close']) / df.tail(days).iloc[0]['close']) * 100
                result += f"  近{days}日涨跌: {change:+.2f}%\n"
        result += "\n"
        
        # 3. 技术指标
        result += "【技术指标】\n"
        ma = calculate_ma(df)
        for key, value in ma.items():
            result += f"  {key}: {value:.2f}元\n"
        
        trend = analyze_trend(df)
        result += f"  趋势: {trend}\n\n"
        
        # 4. MACD
        macd = calculate_macd(df)
        if macd:
            result += "【MACD】\n"
            result += f"  信号: {macd['signal']}\n"
            result += f"  DIF: {macd['DIF']:.2f}, DEA: {macd['DEA']:.2f}\n\n"
        
        # 5. RSI
        rsi = calculate_rsi(df)
        if rsi:
            result += f"【RSI】{rsi:.2f}\n"
            if rsi > 70:
                result += "  状态: 超买，注意回调风险\n\n"
            elif rsi < 30:
                result += "  状态: 超卖，可能存在反弹机会\n\n"
            else:
                result += "  状态: 正常区域\n\n"
        
        # 6. 支撑压力
        sr = get_support_resistance(df)
        if sr:
            result += "【支撑/压力】\n"
            result += f"  支撑位: {sr['support']:.2f}元\n"
            result += f"  压力位: {sr['resistance']:.2f}元\n\n"
        
        # 7. 量能
        volume_ratio = calculate_volume_ratio(df)
        if volume_ratio:
            result += f"【量比】{volume_ratio:.2f}\n"
            if volume_ratio > 2:
                result += "  成交量显著放大，市场关注度高\n"
            elif volume_ratio < 0.5:
                result += "  成交量萎缩，市场观望情绪浓厚\n"
        
        return result
    
    except Exception as e:
        return f"综合分析失败：{str(e)}"


analyze_stock_tool = SimpleTool(
    name="analyze_stock",
    description="对股票进行全面的综合分析，包括基本行情、近期表现、技术指标、趋势判断等。适合回答'分析XX股票'、'XX怎么样'等问题。",
    func=analyze_stock_func,
    args_schema=AnalyzeStockInput
)


# ==================== 导出所有工具 ====================

ALL_TOOLS = [
    get_stock_price_tool,
    get_technical_indicators_tool,
    get_stock_history_tool,
    compare_stocks_tool,
    analyze_stock_tool
]


def get_all_tools():
    """获取所有工具列表"""
    return ALL_TOOLS
