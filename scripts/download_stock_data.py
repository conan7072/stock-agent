"""
股票数据下载脚本

使用 akshare 下载50只热门A股的历史数据（2020-2024）
数据保存为 parquet 格式，便于快速加载
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# 设置UTF-8编码（Windows兼容）
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def download_stock_data():
    """下载股票数据"""
    try:
        import akshare as ak
        import pandas as pd
    except ImportError:
        print("❌ 请先安装 akshare 和 pandas:")
        print("   pip install akshare pandas pyarrow")
        sys.exit(1)
    
    # 保存目录
    data_dir = Path(__file__).parent.parent / "data" / "stocks"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 50只热门A股
    stocks = [
        ("贵州茅台", "600519"),
        ("比亚迪", "002594"),
        ("宁德时代", "300750"),
        ("中国平安", "601318"),
        ("招商银行", "600036"),
        ("五粮液", "000858"),
        ("隆基绿能", "601012"),
        ("药明康德", "603259"),
        ("迈瑞医疗", "300760"),
        ("京东方A", "000725"),
        ("工商银行", "601398"),
        ("建设银行", "601939"),
        ("农业银行", "601288"),
        ("中国银行", "601988"),
        ("兴业银行", "601166"),
        ("中信证券", "600030"),
        ("华泰证券", "601688"),
        ("海天味业", "603288"),
        ("伊利股份", "600887"),
        ("美的集团", "000333"),
        ("格力电器", "000651"),
        ("海康威视", "002415"),
        ("立讯精密", "002475"),
        ("恒瑞医药", "600276"),
        ("长江电力", "600900"),
        ("万科A", "000002"),
        ("保利发展", "600048"),
        ("中国石油", "601857"),
        ("中国石化", "600028"),
        ("中国神华", "601088"),
        ("紫金矿业", "601899"),
        ("山西汾酒", "600809"),
        ("泸州老窖", "000568"),
        ("洋河股份", "002304"),
        ("古井贡酒", "000596"),
        ("中国中免", "601888"),
        ("三一重工", "600031"),
        ("中联重科", "000157"),
        ("徐工机械", "000425"),
        ("上海机场", "600009"),
        ("白云机场", "600004"),
        ("顺丰控股", "002352"),
        ("中通快递", "ZTO"),  # 美股
        ("东方财富", "300059"),
        ("同花顺", "300033"),
        ("宝钢股份", "600019"),
        ("华友钴业", "603799"),
        ("赣锋锂业", "002460"),
        ("天齐锂业", "002466"),
        ("亿纬锂能", "300014"),
    ]
    
    print("=" * 60)
    print("[下载] 股票数据下载工具")
    print("=" * 60)
    print(f"[路径] 保存位置: {data_dir}")
    print(f"[数量] 股票数量: {len(stocks)} 只")
    print(f"[范围] 数据范围: 2020-01-01 至今")
    print()
    
    # 日期范围
    start_date = "20200101"
    end_date = datetime.now().strftime("%Y%m%d")
    
    success_count = 0
    failed_stocks = []
    
    print("⏳ 开始下载数据...")
    print()
    
    for i, (name, code) in enumerate(stocks, 1):
        print(f"[{i}/{len(stocks)}] {name} ({code})...", end=" ")
        
        try:
            # 跳过美股（需要不同的API）
            if not code.isdigit():
                print("跳过 (非A股)")
                continue
            
            # 下载数据
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"  # 前复权
            )
            
            if df.empty:
                print("[FAIL] 无数据")
                failed_stocks.append(name)
                continue
            
            # 重命名列为英文
            df = df.rename(columns={
                "日期": "date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume",
                "成交额": "amount",
                "振幅": "amplitude",
                "涨跌幅": "change_pct",
                "涨跌额": "change",
                "换手率": "turnover"
            })
            
            # 添加股票信息
            df["stock_name"] = name
            df["stock_code"] = code
            
            # 保存为parquet
            file_path = data_dir / f"{name}_{code}.parquet"
            df.to_parquet(file_path, index=False)
            
            print(f"[OK] {len(df)} 条记录")
            success_count += 1
            
        except Exception as e:
            print(f"[FAIL] 失败: {str(e)[:30]}")
            failed_stocks.append(name)
    
    print()
    print("=" * 60)
    print("[完成] 下载完成")
    print("=" * 60)
    print(f"[成功] 成功: {success_count} 只")
    print(f"[失败] 失败: {len(failed_stocks)} 只")
    
    if failed_stocks:
        print(f"   失败列表: {', '.join(failed_stocks)}")
    
    print()
    print(f"[路径] 数据位置: {data_dir}")
    print(f"[文件] 文件数量: {len(list(data_dir.glob('*.parquet')))} 个")
    
    # 计算总大小
    total_size = sum(f.stat().st_size for f in data_dir.glob('*.parquet'))
    print(f"[大小] 总大小: {total_size / 1024 / 1024:.1f} MB")
    
    print()
    print("[下一步]:")
    print("  1. 构建向量数据库:")
    print("     python scripts/build_vectordb.py")
    print()
    
    return success_count > 0

def check_data_exists():
    """检查数据是否已存在"""
    data_dir = Path(__file__).parent.parent / "data" / "stocks"
    
    if not data_dir.exists():
        return False
    
    files = list(data_dir.glob('*.parquet'))
    
    if files:
        print(f"[已存在] 已有 {len(files)} 个股票数据文件")
        print(f"[位置] {data_dir}")
        return True
    
    return False

def main():
    """主函数"""
    print()
    print("=" * 60)
    print("[工具] 股票数据下载工具 (akshare)")
    print("=" * 60)
    print()
    
    # 检查是否已有数据
    if check_data_exists():
        choice = input("数据已存在，是否重新下载? [y/N]: ").strip().lower()
        if choice != 'y':
            print("[跳过] 跳过下载")
            return
    
    # 开始下载
    success = download_stock_data()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
