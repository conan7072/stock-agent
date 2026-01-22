"""
向量数据库构建脚本

读取 data/knowledge/ 目录下的所有markdown文件，
使用 bge-small-zh-v1.5 进行向量化，
存储到 Chroma 向量数据库
"""

import sys
from pathlib import Path
from typing import List

def load_documents():
    """加载知识库文档"""
    knowledge_dir = Path(__file__).parent.parent / "data" / "knowledge"
    
    if not knowledge_dir.exists():
        print(f"❌ 知识库目录不存在: {knowledge_dir}")
        return []
    
    # 查找所有markdown文件
    md_files = list(knowledge_dir.rglob("*.md"))
    
    if not md_files:
        print(f"⚠️  未找到任何markdown文件")
        return []
    
    print(f"📚 找到 {len(md_files)} 个文档文件")
    
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
            
            print(f"   ✅ {relative_path}")
            
        except Exception as e:
            print(f"   ❌ {file_path.name}: {e}")
    
    return documents

def split_documents(documents: List[dict], chunk_size: int = 500, chunk_overlap: int = 50):
    """分割文档为小块"""
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        print("❌ 请先安装 langchain:")
        print("   pip install langchain")
        sys.exit(1)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
    )
    
    chunks = []
    
    for doc in documents:
        texts = text_splitter.split_text(doc["content"])
        
        for i, text in enumerate(texts):
            chunks.append({
                "content": text,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": i,
                    "total_chunks": len(texts)
                }
            })
    
    print(f"📄 文档分割完成: {len(chunks)} 个块")
    
    return chunks

def build_vectordb(chunks: List[dict]):
    """构建向量数据库"""
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
    except ImportError:
        print("❌ 请先安装依赖:")
        print("   pip install langchain-community sentence-transformers chromadb")
        sys.exit(1)
    
    # 向量数据库保存路径
    vectordb_dir = Path(__file__).parent.parent / "data" / "vector_db"
    vectordb_dir.mkdir(parents=True, exist_ok=True)
    
    print()
    print("🔧 初始化向量模型: bge-small-zh-v1.5")
    print("   首次使用会自动下载模型（约90MB）...")
    
    # 创建 embedding 模型
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    print("   ✅ 模型加载完成")
    print()
    print("🔄 向量化文档...")
    
    # 准备数据
    texts = [chunk["content"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    
    # 创建向量数据库
    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=str(vectordb_dir)
    )
    
    # 持久化
    vectordb.persist()
    
    print("   ✅ 向量化完成")
    
    return vectordb, vectordb_dir

def test_retrieval(vectordb):
    """测试检索功能"""
    print()
    print("🧪 测试检索功能...")
    print()
    
    test_queries = [
        "什么是股票？",
        "如何计算市盈率？",
        "MACD指标怎么使用？"
    ]
    
    for query in test_queries:
        print(f"查询: {query}")
        results = vectordb.similarity_search(query, k=2)
        
        for i, doc in enumerate(results, 1):
            print(f"   [{i}] 来源: {doc.metadata.get('source', 'unknown')}")
            preview = doc.page_content[:100].replace('\n', ' ')
            print(f"       内容: {preview}...")
        print()

def main():
    """主函数"""
    print()
    print("=" * 60)
    print("🔧 向量数据库构建工具")
    print("=" * 60)
    print()
    
    # 1. 加载文档
    print("📚 步骤1: 加载知识库文档")
    documents = load_documents()
    
    if not documents:
        print("❌ 没有可用的文档")
        sys.exit(1)
    
    print()
    
    # 2. 分割文档
    print("📄 步骤2: 分割文档")
    chunks = split_documents(documents, chunk_size=500, chunk_overlap=50)
    print()
    
    # 3. 构建向量数据库
    print("🔧 步骤3: 构建向量数据库")
    vectordb, vectordb_dir = build_vectordb(chunks)
    
    # 4. 测试检索
    test_retrieval(vectordb)
    
    print("=" * 60)
    print("✅ 向量数据库构建完成！")
    print("=" * 60)
    print(f"📁 位置: {vectordb_dir}")
    print(f"📊 文档数: {len(chunks)} 个块")
    
    # 计算大小
    total_size = sum(f.stat().st_size for f in vectordb_dir.rglob('*') if f.is_file())
    print(f"💾 大小: {total_size / 1024 / 1024:.1f} MB")
    
    print()
    print("🔧 下一步:")
    print("  1. 启动服务:")
    print("     python server/start_server.py")
    print()

if __name__ == "__main__":
    main()
