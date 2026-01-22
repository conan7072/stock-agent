"""
股票数据加载器

从parquet文件中加载股票数据
"""

from pathlib import Path
from typing import Optional, Dict, List
import pandas as pd


class StockDataLoader:
    """股票数据加载器"""
    
    def __init__(self, data_dir: str = "./data/stocks"):
        self.data_dir = Path(data_dir)
        self._cache: Dict[str, pd.DataFrame] = {}
        self._stock_map: Optional[Dict[str, str]] = None
    
    def _build_stock_map(self):
        """构建股票名称到文件的映射"""
        if self._stock_map is not None:
            return
        
        self._stock_map = {}
        
        if not self.data_dir.exists():
            return
        
        for file_path in self.data_dir.glob("*.parquet"):
            # 文件名格式：股票名称_代码.parquet
            name = file_path.stem
            if '_' in name:
                stock_name, stock_code = name.rsplit('_', 1)
                # 支持按名称和代码查询
                self._stock_map[stock_name] = file_path
                self._stock_map[stock_code] = file_path
                self._stock_map[stock_name.lower()] = file_path
    
    def get_stock_data(
        self, 
        stock: str, 
        use_cache: bool = True
    ) -> Optional[pd.DataFrame]:
        """
        获取股票数据
        
        Args:
            stock: 股票名称或代码（如"比亚迪"或"002594"）
            use_cache: 是否使用缓存
            
        Returns:
            股票数据DataFrame，如果不存在则返回None
        """
        self._build_stock_map()
        
        # 查找文件
        stock_key = stock.lower() if stock else ""
        
        if stock_key not in self._stock_map:
            # 尝试模糊匹配
            for key in self._stock_map.keys():
                if stock in key or key in stock:
                    stock_key = key
                    break
            else:
                return None
        
        file_path = self._stock_map[stock_key]
        
        # 使用缓存
        if use_cache and str(file_path) in self._cache:
            return self._cache[str(file_path)]
        
        # 读取数据
        try:
            df = pd.read_parquet(file_path)
            
            if use_cache:
                self._cache[str(file_path)] = df
            
            return df
        except Exception as e:
            print(f"读取股票数据失败 {stock}: {e}")
            return None
    
    def list_available_stocks(self) -> List[Dict[str, str]]:
        """
        列出所有可用的股票
        
        Returns:
            股票列表，每项包含name和code
        """
        self._build_stock_map()
        
        stocks = []
        seen = set()
        
        for key, file_path in self._stock_map.items():
            if file_path in seen:
                continue
            
            seen.add(file_path)
            
            name = file_path.stem
            if '_' in name:
                stock_name, stock_code = name.rsplit('_', 1)
                stocks.append({
                    "name": stock_name,
                    "code": stock_code
                })
        
        return stocks
    
    def get_latest_price(self, stock: str) -> Optional[Dict]:
        """
        获取最新价格
        
        Args:
            stock: 股票名称或代码
            
        Returns:
            包含最新价格信息的字典
        """
        df = self.get_stock_data(stock)
        
        if df is None or len(df) == 0:
            return None
        
        latest = df.iloc[-1]
        
        return {
            "date": latest["date"],
            "open": float(latest["open"]),
            "close": float(latest["close"]),
            "high": float(latest["high"]),
            "low": float(latest["low"]),
            "volume": int(latest["volume"]),
            "change_pct": float(latest["change_pct"]) if "change_pct" in latest else None
        }
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()


# 全局实例
_loader: Optional[StockDataLoader] = None


def get_loader(data_dir: str = "./data/stocks") -> StockDataLoader:
    """获取全局加载器实例"""
    global _loader
    
    if _loader is None:
        _loader = StockDataLoader(data_dir)
    
    return _loader
