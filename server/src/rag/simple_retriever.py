"""
简化版RAG检索器

基于关键词匹配的知识库检索，无需GPU
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


class SimpleRetriever:
    """简单的关键词检索器"""
    
    def __init__(self, index_path: str = "./data/knowledge_index.json"):
        self.index_path = Path(index_path)
        self.index: List[Dict] = []
        self.load_index()
    
    def load_index(self):
        """加载索引"""
        if not self.index_path.exists():
            print(f"警告：索引文件不存在 {self.index_path}")
            return
        
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
            print(f"已加载 {len(self.index)} 条知识库索引")
        except Exception as e:
            print(f"加载索引失败：{e}")
    
    def search(
        self, 
        query: str, 
        top_k: int = 3,
        min_score: float = 0.0
    ) -> List[Dict]:
        """
        搜索相关知识
        
        Args:
            query: 查询字符串
            top_k: 返回前K个结果
            min_score: 最小匹配分数
            
        Returns:
            匹配的知识列表
        """
        if not self.index:
            return []
        
        # 提取查询关键词
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        results = []
        
        for doc in self.index:
            # 计算匹配分数
            score = 0.0
            content = doc.get('content', '').lower()
            title = doc.get('title', '').lower()
            keywords = doc.get('keywords', [])
            
            # 完全匹配（高分）
            if query_lower in content or query_lower in title:
                score += 10.0
            
            # 关键词匹配
            for kw in keywords:
                if kw.lower() in query_lower:
                    score += 5.0
                if kw.lower() in query_words:
                    score += 3.0
            
            # 词语匹配
            content_words = set(content.split())
            title_words = set(title.split())
            
            common_words = query_words & (content_words | title_words)
            score += len(common_words) * 0.5
            
            if score > min_score:
                results.append({
                    'content': doc.get('content', ''),
                    'title': doc.get('title', ''),
                    'source': doc.get('source', ''),
                    'score': score
                })
        
        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_k]
    
    def get_context(
        self, 
        query: str, 
        max_length: int = 500
    ) -> str:
        """
        获取上下文字符串
        
        Args:
            query: 查询字符串
            max_length: 最大长度
            
        Returns:
            拼接的上下文
        """
        results = self.search(query, top_k=3)
        
        if not results:
            return ""
        
        context_parts = []
        current_length = 0
        
        for result in results:
            content = result['content']
            title = result.get('title', '')
            
            # 格式化内容
            if title:
                part = f"【{title}】\n{content}"
            else:
                part = content
            
            # 检查长度限制
            if current_length + len(part) > max_length:
                # 截断
                remaining = max_length - current_length
                if remaining > 100:  # 至少保留100字符
                    part = part[:remaining] + "..."
                    context_parts.append(part)
                break
            
            context_parts.append(part)
            current_length += len(part)
        
        return "\n\n---\n\n".join(context_parts)
    
    def is_knowledge_query(self, query: str) -> bool:
        """
        判断是否是知识查询
        
        Args:
            query: 查询字符串
            
        Returns:
            是否是知识查询
        """
        # 知识查询的关键词
        knowledge_keywords = [
            "什么是", "如何", "怎么", "为什么", "哪些",
            "概念", "定义", "含义", "解释", "介绍",
            "原理", "方法", "步骤", "技巧", "知识",
            "什么叫", "啥是", "啥叫"
        ]
        
        query_lower = query.lower()
        
        return any(kw in query_lower for kw in knowledge_keywords)
    
    def get_relevant_knowledge(self, query: str) -> Optional[str]:
        """
        获取相关知识（如果有）
        
        Args:
            query: 查询字符串
            
        Returns:
            相关知识或None
        """
        # 判断是否需要知识库
        if not self.is_knowledge_query(query):
            # 即使不是典型的知识查询，也尝试搜索一下
            results = self.search(query, top_k=1, min_score=5.0)
            if results:
                return results[0]['content']
            return None
        
        # 获取上下文
        context = self.get_context(query, max_length=800)
        
        return context if context else None


# 全局实例
_retriever: Optional[SimpleRetriever] = None


def get_retriever(index_path: str = "./data/knowledge_index.json") -> SimpleRetriever:
    """获取全局检索器实例"""
    global _retriever
    
    if _retriever is None:
        _retriever = SimpleRetriever(index_path)
    
    return _retriever
