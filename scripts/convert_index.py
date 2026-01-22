"""
转换向量数据库索引格式

将documents.json转换为simple_retriever需要的格式
"""

import sys
import json
from pathlib import Path
import re

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def extract_keywords(content: str) -> list:
    """从内容中提取关键词"""
    keywords = []
    
    # 常见的金融关键词
    finance_keywords = [
        "股票", "价格", "市盈率", "市净率", "收益", "股息", "红利",
        "涨停", "跌停", "均线", "MA", "MACD", "RSI", "BOLL", "KDJ",
        "技术分析", "基本面", "趋势", "支撑", "压力", "金叉", "死叉",
        "超买", "超卖", "成交量", "换手率", "委比", "量比",
        "A股", "上交所", "深交所", "创业板", "科创板",
        "涨跌幅", "交易", "买入", "卖出", "持仓", "止损"
    ]
    
    content_lower = content.lower()
    
    for keyword in finance_keywords:
        if keyword in content or keyword.lower() in content_lower:
            keywords.append(keyword)
    
    # 提取标题（## 开头的）
    titles = re.findall(r'##\s+([^\n]+)', content)
    keywords.extend(titles[:5])  # 最多添加5个标题作为关键词
    
    return list(set(keywords))  # 去重


def convert_index():
    """转换索引格式"""
    print("=" * 60)
    print("索引格式转换工具")
    print("=" * 60)
    print()
    
    # 读取documents.json
    input_file = Path("data/vector_db/documents.json")
    output_file = Path("data/knowledge_index.json")
    
    if not input_file.exists():
        print(f"错误：找不到输入文件 {input_file}")
        return
    
    print(f"[1] 读取输入文件: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    documents = data.get('documents', [])
    print(f"    找到 {len(documents)} 个文档")
    
    # 转换格式
    print(f"\n[2] 转换格式...")
    
    converted = []
    
    for doc in documents:
        content = doc.get('content', '')
        metadata = doc.get('metadata', {})
        source = metadata.get('source', '')
        
        # 提取标题（第一行 # 开头的）
        title_match = re.search(r'^#\s+([^\n]+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""
        
        # 提取关键词
        keywords = extract_keywords(content)
        
        converted.append({
            'content': content,
            'title': title,
            'source': source,
            'keywords': keywords
        })
    
    print(f"    转换完成: {len(converted)} 条记录")
    
    # 保存
    print(f"\n[3] 保存到: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)
    
    print(f"    文件大小: {output_file.stat().st_size / 1024:.1f} KB")
    
    # 统计关键词
    all_keywords = set()
    for item in converted:
        all_keywords.update(item['keywords'])
    
    print(f"    关键词数量: {len(all_keywords)}")
    
    print("\n" + "=" * 60)
    print("转换完成！")
    print("=" * 60)
    
    # 测试
    print("\n[TEST] 测试加载...")
    
    with open(output_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    print(f"成功加载 {len(test_data)} 条记录")
    
    if test_data:
        print("\n示例记录:")
        sample = test_data[0]
        print(f"  标题: {sample.get('title', '无')}")
        print(f"  来源: {sample.get('source', '无')}")
        print(f"  关键词: {', '.join(sample.get('keywords', [])[:10])}")
        print(f"  内容长度: {len(sample.get('content', ''))} 字符")


if __name__ == "__main__":
    convert_index()
