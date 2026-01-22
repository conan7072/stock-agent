"""
股票技术指标计算

计算常用的技术指标：MA, MACD, RSI, BOLL等
"""

from typing import Dict, Optional
import pandas as pd
import numpy as np


def calculate_ma(df: pd.DataFrame, periods: list = [5, 10, 20, 60]) -> Dict[str, float]:
    """
    计算移动平均线
    
    Args:
        df: 股票数据DataFrame
        periods: 计算周期列表
        
    Returns:
        各周期的MA值
    """
    result = {}
    
    for period in periods:
        if len(df) >= period:
            ma_value = df.tail(period)["close"].mean()
            result[f"MA{period}"] = round(ma_value, 2)
    
    return result


def calculate_macd(
    df: pd.DataFrame, 
    fast: int = 12, 
    slow: int = 26, 
    signal: int = 9
) -> Optional[Dict]:
    """
    计算MACD指标
    
    Args:
        df: 股票数据DataFrame
        fast: 快线周期
        slow: 慢线周期
        signal: 信号线周期
        
    Returns:
        MACD指标值
    """
    if len(df) < slow + signal:
        return None
    
    close = df["close"]
    
    # 计算EMA
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    
    # DIF
    dif = ema_fast - ema_slow
    
    # DEA (DIF的EMA)
    dea = dif.ewm(span=signal, adjust=False).mean()
    
    # MACD柱
    macd = (dif - dea) * 2
    
    # 返回最新值
    return {
        "DIF": round(dif.iloc[-1], 2),
        "DEA": round(dea.iloc[-1], 2),
        "MACD": round(macd.iloc[-1], 2),
        "signal": "金叉" if dif.iloc[-1] > dea.iloc[-1] and dif.iloc[-2] <= dea.iloc[-2] else 
                  "死叉" if dif.iloc[-1] < dea.iloc[-1] and dif.iloc[-2] >= dea.iloc[-2] else "持有"
    }


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> Optional[float]:
    """
    计算RSI指标
    
    Args:
        df: 股票数据DataFrame
        period: 计算周期
        
    Returns:
        RSI值
    """
    if len(df) < period + 1:
        return None
    
    close = df["close"]
    
    # 计算价格变化
    delta = close.diff()
    
    # 分离上涨和下跌
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # 计算平均涨跌
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # 计算RS和RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    latest_rsi = rsi.iloc[-1]
    
    return round(latest_rsi, 2)


def calculate_boll(
    df: pd.DataFrame, 
    period: int = 20, 
    std_dev: float = 2.0
) -> Optional[Dict]:
    """
    计算布林带指标
    
    Args:
        df: 股票数据DataFrame
        period: 计算周期
        std_dev: 标准差倍数
        
    Returns:
        布林带上中下轨
    """
    if len(df) < period:
        return None
    
    close = df["close"]
    
    # 中轨（MA）
    middle = close.rolling(window=period).mean()
    
    # 标准差
    std = close.rolling(window=period).std()
    
    # 上下轨
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    
    current_price = close.iloc[-1]
    
    return {
        "upper": round(upper.iloc[-1], 2),
        "middle": round(middle.iloc[-1], 2),
        "lower": round(lower.iloc[-1], 2),
        "current": round(current_price, 2),
        "position": "上轨附近" if current_price > upper.iloc[-1] * 0.98 else
                    "下轨附近" if current_price < lower.iloc[-1] * 1.02 else
                    "中轨附近"
    }


def analyze_trend(df: pd.DataFrame) -> str:
    """
    分析趋势
    
    Args:
        df: 股票数据DataFrame
        
    Returns:
        趋势描述
    """
    if len(df) < 20:
        return "数据不足"
    
    ma = calculate_ma(df, [5, 10, 20])
    current_price = df.iloc[-1]["close"]
    
    # 判断多空排列
    if "MA5" in ma and "MA10" in ma and "MA20" in ma:
        if current_price > ma["MA5"] > ma["MA10"] > ma["MA20"]:
            return "强势上涨（多头排列）"
        elif current_price < ma["MA5"] < ma["MA10"] < ma["MA20"]:
            return "弱势下跌（空头排列）"
    
    # 判断近期走势
    recent_5 = df.tail(5)
    change_5d = ((recent_5.iloc[-1]["close"] - recent_5.iloc[0]["close"]) / recent_5.iloc[0]["close"]) * 100
    
    if change_5d > 5:
        return "短期强势上涨"
    elif change_5d < -5:
        return "短期快速下跌"
    
    return "震荡整理"


def get_support_resistance(df: pd.DataFrame, period: int = 20) -> Dict:
    """
    计算支撑位和压力位
    
    Args:
        df: 股票数据DataFrame
        period: 计算周期
        
    Returns:
        支撑位和压力位
    """
    if len(df) < period:
        return {}
    
    recent = df.tail(period)
    
    support = recent["low"].min()
    resistance = recent["high"].max()
    
    return {
        "support": round(support, 2),
        "resistance": round(resistance, 2)
    }


def calculate_volume_ratio(df: pd.DataFrame) -> Optional[float]:
    """
    计算量比
    
    Args:
        df: 股票数据DataFrame
        
    Returns:
        量比
    """
    if len(df) < 6:
        return None
    
    # 今日成交量
    current_volume = df.iloc[-1]["volume"]
    
    # 过去5日平均成交量
    avg_volume = df.tail(6).iloc[:-1]["volume"].mean()
    
    if avg_volume == 0:
        return None
    
    volume_ratio = current_volume / avg_volume
    
    return round(volume_ratio, 2)
