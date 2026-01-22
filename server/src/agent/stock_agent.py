"""
股票咨询Agent

基于LangGraph的股票咨询Agent，集成工具和RAG
"""

from typing import TypedDict, Annotated, Sequence, Literal
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from server.src.llm.factory import create_llm_from_config_file
from server.src.tools.stock_tools import get_all_tools
from server.src.rag.simple_retriever import get_retriever


# ==================== 状态定义 ====================

class AgentState(TypedDict):
    """Agent状态"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    knowledge_context: str  # RAG检索的知识
    tool_results: list  # 工具调用结果
    next_action: str  # 下一步动作


# ==================== 简化版Agent ====================

class SimpleStockAgent:
    """简化版股票咨询Agent（无GPU版本）"""
    
    def __init__(self, config_path: str = "./server/configs/server_config.yaml"):
        # 初始化LLM
        self.llm = create_llm_from_config_file(config_path)
        
        # 初始化工具
        self.tools = {tool.name: tool for tool in get_all_tools()}
        
        # 初始化RAG
        self.retriever = get_retriever()
        
        print(f"Agent初始化完成：LLM={type(self.llm).__name__}, 工具数={len(self.tools)}")
    
    def route_query(self, query: str) -> Literal["tool", "knowledge", "direct"]:
        """
        路由查询到不同的处理路径
        
        Args:
            query: 用户查询
            
        Returns:
            路由结果：tool（工具）、knowledge（知识库）、direct（直接回答）
        """
        query_lower = query.lower()
        
        # 工具查询关键词
        tool_keywords = [
            "价格", "多少钱", "股价", "行情",
            "技术指标", "MACD", "RSI", "均线", "MA",
            "历史", "走势", "表现",
            "对比", "比较",
            "分析"
        ]
        
        # 知识查询关键词
        knowledge_keywords = [
            "什么是", "如何", "怎么", "为什么", "哪些",
            "概念", "定义", "含义", "解释", "介绍"
        ]
        
        # 判断
        has_tool_keyword = any(kw in query for kw in tool_keywords)
        has_knowledge_keyword = any(kw in query for kw in knowledge_keywords)
        
        if has_tool_keyword and not has_knowledge_keyword:
            return "tool"
        elif has_knowledge_keyword:
            return "knowledge"
        else:
            # 同时包含或都不包含，尝试工具
            return "tool"
    
    def select_tool(self, query: str) -> str:
        """
        选择合适的工具
        
        Args:
            query: 用户查询
            
        Returns:
            工具名称
        """
        query_lower = query.lower()
        
        # 简单的规则匹配
        if "价格" in query or "多少钱" in query or "股价" in query:
            return "get_stock_price"
        elif "技术指标" in query or "MACD" in query or "RSI" in query:
            return "get_technical_indicators"
        elif "历史" in query or "最近" in query or "走势" in query:
            return "get_stock_history"
        elif "对比" in query or "比较" in query:
            return "compare_stocks"
        elif "分析" in query:
            return "analyze_stock"
        else:
            # 默认使用综合分析
            return "analyze_stock"
    
    def extract_stock_name(self, query: str) -> str:
        """
        从查询中提取股票名称
        
        Args:
            query: 用户查询
            
        Returns:
            股票名称
        """
        # 常见股票列表（前10只）
        common_stocks = [
            "比亚迪", "宁德时代", "贵州茅台", "中国平安", "招商银行",
            "工商银行", "建设银行", "中国石油", "中国石化", "五粮液"
        ]
        
        for stock in common_stocks:
            if stock in query:
                return stock
        
        # 如果没找到，返回查询本身（让工具处理）
        words = query.replace("？", "").replace("?", "").split()
        for word in words:
            if len(word) >= 2 and word not in ["股票", "价格", "怎么样", "如何"]:
                return word
        
        return "比亚迪"  # 默认
    
    def call_tool(self, tool_name: str, **kwargs) -> str:
        """
        调用工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            工具输出
        """
        if tool_name not in self.tools:
            return f"工具 {tool_name} 不存在"
        
        tool = self.tools[tool_name]
        
        try:
            result = tool.func(**kwargs)
            return result
        except Exception as e:
            return f"工具调用失败：{str(e)}"
    
    def query(self, user_query: str) -> str:
        """
        处理用户查询
        
        Args:
            user_query: 用户查询
            
        Returns:
            回答
        """
        # 1. 路由
        route = self.route_query(user_query)
        
        print(f"\n[Agent] 查询路由: {route}")
        
        if route == "knowledge":
            # 知识库查询
            print("[Agent] 从知识库检索...")
            knowledge = self.retriever.get_relevant_knowledge(user_query)
            
            if knowledge:
                # 使用LLM基于知识生成回答
                prompt = f"""请基于以下知识回答用户的问题。

用户问题：{user_query}

相关知识：
{knowledge}

请用简洁明了的语言回答，如果知识库中的信息不足，可以适当补充你的理解。"""
                
                # 使用同步方法
                if hasattr(self.llm, 'generate_sync'):
                    answer = self.llm.generate_sync(prompt)
                else:
                    # 如果没有同步方法，尝试异步方法
                    import asyncio
                    answer = asyncio.run(self.llm.generate(prompt))
                return answer
            else:
                return "抱歉，我在知识库中没有找到相关信息。您可以换个方式提问。"
        
        elif route == "tool":
            # 工具调用
            print("[Agent] 调用工具...")
            
            # 选择工具
            tool_name = self.select_tool(user_query)
            print(f"[Agent] 选择工具: {tool_name}")
            
            # 提取参数
            if tool_name == "compare_stocks":
                # 对比工具需要股票列表
                # 简单处理：提取多个股票名
                stocks = []
                for stock in ["比亚迪", "宁德时代", "贵州茅台", "中国平安", "招商银行"]:
                    if stock in user_query:
                        stocks.append(stock)
                
                if len(stocks) < 2:
                    stocks = ["比亚迪", "宁德时代", "贵州茅台"]  # 默认对比
                
                tool_result = self.call_tool(tool_name, stocks=stocks)
            else:
                # 其他工具需要股票名称
                stock_name = self.extract_stock_name(user_query)
                print(f"[Agent] 提取股票: {stock_name}")
                
                if tool_name == "get_stock_history":
                    # 历史数据工具可能需要天数参数
                    days = 10  # 默认10天
                    if "5" in user_query or "五" in user_query:
                        days = 5
                    elif "20" in user_query or "二十" in user_query:
                        days = 20
                    
                    tool_result = self.call_tool(tool_name, stock=stock_name, days=days)
                else:
                    tool_result = self.call_tool(tool_name, stock=stock_name)
            
            print(f"[Agent] 工具执行完成")
            
            # 使用LLM总结工具结果
            prompt = f"""请基于工具的查询结果，回答用户的问题。

用户问题：{user_query}

工具结果：
{tool_result}

请用自然、友好的语言总结这些信息，给用户一个清晰的回答。如果有投资建议的需求，请务必提醒"投资有风险，仅供参考"。"""
            
            # 使用同步方法
            if hasattr(self.llm, 'generate_sync'):
                answer = self.llm.generate_sync(prompt)
            else:
                import asyncio
                answer = asyncio.run(self.llm.generate(prompt))
            return answer
        
        else:
            # 直接回答
            print("[Agent] 直接回答...")
            if hasattr(self.llm, 'generate_sync'):
                answer = self.llm.generate_sync(user_query)
            else:
                import asyncio
                answer = asyncio.run(self.llm.generate(user_query))
            return answer
    
    def chat(self, user_query: str) -> str:
        """
        聊天接口（和query相同，但名字更友好）
        
        Args:
            user_query: 用户查询
            
        Returns:
            回答
        """
        return self.query(user_query)


# ==================== 全局实例 ====================

_agent: SimpleStockAgent = None


def get_agent(config_path: str = "./server/configs/server_config.yaml") -> SimpleStockAgent:
    """获取全局Agent实例"""
    global _agent
    
    if _agent is None:
        _agent = SimpleStockAgent(config_path)
    
    return _agent
