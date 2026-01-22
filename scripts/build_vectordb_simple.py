"""
向量数据库构建脚本（简化版）

读取知识库文档，使用简单的方法构建向量数据库
无需GPU，无需PyTorch
"""

import sys
import json
from pathlib import Path
from typing import List, Dict

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def load_documents() -> List[Dict]:
    """加载知识库文档"""
    knowledge_dir = Path(__file__).parent.parent / "data" / "knowledge"
    
    if not knowledge_dir.exists():
        print(f"[ERROR] 知识库目录不存在: {knowledge_dir}")
        return []
    
    # 查找所有markdown文件
    md_files = list(knowledge_dir.rglob("*.md"))
    
    if not md_files:
        print(f"[WARN] 未找到任何markdown文件")
        return []
    
    print(f"[INFO] 找到 {len(md_files)} 个文档文件")
    
    documents = []
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取文件信息
            relative_path = file_path.relative_to(knowledge_dir)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else "general"
            
            documents.append({
                "content": content,
                "metadata": {
                    "source": str(relative_path),
                    "category": category,
                    "filename": file_path.name
                }
            })
            
            print(f"   [OK] {relative_path}")
            
        except Exception as e:
            print(f"   [ERROR] {file_path.name}: {e}")
    
    return documents


def split_documents(documents: List[Dict], chunk_size: int = 500) -> List[Dict]:
    """简单分割文档"""
    chunks = []
    
    for doc in documents:
        content = doc["content"]
        
        # 简单分割：按段落
        paragraphs = content.split('\n\n')
        
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append({
                        "content": current_chunk.strip(),
                        "metadata": doc["metadata"].copy()
                    })
                current_chunk = para + "\n\n"
        
        # 添加最后一个块
        if current_chunk:
            chunks.append({
                "content": current_chunk.strip(),
                "metadata": doc["metadata"].copy()
            })
    
    print(f"[INFO] 文档分割完成: {len(chunks)} 个块")
    return chunks


def build_simple_vectordb(chunks: List[Dict]) -> Path:
    """构建简单的JSON数据库（无需向量化）"""
    # 向量数据库保存路径
    vectordb_dir = Path(__file__).parent.parent / "data" / "vector_db"
    vectordb_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存为JSON格式
    json_file = vectordb_dir / "documents.json"
    
    # 准备数据
    data = {
        "documents": chunks,
        "count": len(chunks),
        "version": "1.0"
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 数据已保存到: {json_file}")
    print(f"[INFO] 共 {len(chunks)} 个文档块")
    
    return vectordb_dir


def create_index(chunks: List[Dict]):
    """创建简单的关键词索引"""
    vectordb_dir = Path(__file__).parent.parent / "data" / "vector_db"
    
    # 提取关键词
    index = {}
    for i, chunk in enumerate(chunks):
        content = chunk["content"].lower()
        # 提取一些关键词
        keywords = set()
        
        # 股票相关关键词
        stock_keywords = [
            "股票", "股价", "市盈率", "市净率", "涨跌", "买入", "卖出",
            "ma", "macd", "rsi", "kdj", "均线", "技术指标",
            "pe", "pb", "roe", "财务", "分红", "估值"
        ]
        
        for keyword in stock_keywords:
            if keyword in content:
                if keyword not in index:
                    index[keyword] = []
                index[keyword].append(i)
    
    # 保存索引
    index_file = vectordb_dir / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 索引已创建: {len(index)} 个关键词")


def test_search(chunks: List[Dict]):
    """测试简单搜索"""
    print()
    print("[TEST] 测试检索功能...")
    print()
    
    test_queries = [
        "什么是股票？",
        "如何计算市盈率？",
        "MACD指标怎么使用？"
    ]
    
    for query in test_queries:
        print(f"[查询] {query}")
        
        # 简单关键词匹配
        query_lower = query.lower()
        matches = []
        
        for i, chunk in enumerate(chunks):
            content_lower = chunk["content"].lower()
            # 计算相关性得分（简单的关键词匹配）
            score = 0
            for char in query:
                if char in content_lower:
                    score += 1
            
            if score > len(query) * 0.3:  # 至少30%匹配
                matches.append((i, score, chunk))
        
        # 按得分排序
        matches.sort(key=lambda x: x[1], reverse=True)
        
        # 显示前2个结果
        for idx, (i, score, chunk) in enumerate(matches[:2], 1):
            print(f"   [{idx}] 来源: {chunk['metadata'].get('source', 'unknown')}")
            preview = chunk['content'][:100].replace('\n', ' ')
            print(f"       内容: {preview}...")
        print()


def main():
    """主函数"""
    print()
    print("=" * 60)
    print("[工具] 向量数据库构建工具（简化版）")
    print("=" * 60)
    print()
    
    # 1. 加载文档
    print("[步骤1] 加载知识库文档")
    documents = load_documents()
    
    if not documents:
        print("[ERROR] 没有可用的文档")
        sys.exit(1)
    
    print()
    
    # 2. 分割文档
    print("[步骤2] 分割文档")
    chunks = split_documents(documents, chunk_size=500)
    print()
    
    # 3. 构建数据库
    print("[步骤3] 构建数据库")
    vectordb_dir = build_simple_vectordb(chunks)
    print()
    
    # 4. 创建索引
    print("[步骤4] 创建关键词索引")
    create_index(chunks)
    print()
    
    # 5. 测试检索
    test_search(chunks)
    
    print("=" * 60)
    print("[SUCCESS] 数据库构建完成！")
    print("=" * 60)
    print(f"[位置] {vectordb_dir}")
    print(f"[文档] {len(chunks)} 个块")
    
    # 计算大小
    json_file = vectordb_dir / "documents.json"
    if json_file.exists():
        size_kb = json_file.stat().st_size / 1024
        print(f"[大小] {size_kb:.1f} KB")
    
    print()
    print("[INFO] 说明:")
    print("   - 使用简化版数据库（JSON格式）")
    print("   - 基于关键词匹配的检索")
    print("   - 无需GPU和PyTorch")
    print("   - 后续可升级为真实向量数据库")
    print()


if __name__ == "__main__":
    main()
