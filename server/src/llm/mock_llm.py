"""
Mock LLM实现

用于无GPU环境的开发和测试
模拟ChatGLM3的响应行为
"""

import asyncio
import re
from typing import AsyncIterator, Optional, Dict, Any
from .base import BaseLLM, LLMConfig


class MockLLM(BaseLLM):
    """Mock LLM - 模拟智能响应"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.call_count = 0
        
        # 预设的响应模板
        self.templates = {
            "stock_query": self._generate_stock_response,
            "tool_call": self._generate_tool_call,
            "general": self._generate_general_response,
        }
    
    def generate_sync(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """生成响应（同步版本，用于非async环境）"""
        self.call_count += 1
        
        # 根据prompt内容选择响应类型
        response = self._select_response(prompt)
        
        return response
    
    async def generate(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """生成响应（异步版本）"""
        return self.generate_sync(prompt, max_length, temperature, **kwargs)
    
    async def generate_stream(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """生成响应（流式）"""
        self.call_count += 1
        
        # 生成完整响应
        full_response = self._select_response(prompt)
        
        # 模拟流式输出（每次输出几个字符）
        chunk_size = 5
        for i in range(0, len(full_response), chunk_size):
            chunk = full_response[i:i+chunk_size]
            await asyncio.sleep(0.05)  # 模拟生成延迟
            yield chunk
    
    def _select_response(self, prompt: str) -> str:
        """根据prompt选择合适的响应"""
        prompt_lower = prompt.lower()
        
        # 检测是否是工具调用请求
        if "function" in prompt_lower or "tool" in prompt_lower:
            return self._generate_tool_call(prompt)
        
        # 检测股票查询
        stock_keywords = ["股票", "比亚迪", "茅台", "宁德时代", "股价", "分析", "投资"]
        if any(kw in prompt for kw in stock_keywords):
            return self._generate_stock_response(prompt)
        
        # 通用响应
        return self._generate_general_response(prompt)
    
    def _generate_tool_call(self, prompt: str) -> str:
        """生成工具调用响应"""
        # 提取股票名称
        stock_name = self._extract_stock_name(prompt)
        
        if stock_name:
            return f"""我需要获取{stock_name}的相关数据来进行分析。

让我调用以下工具：
1. get_stock_price("{stock_name}", "1month") - 获取最近一个月的价格数据
2. get_financial_indicators("{stock_name}") - 获取财务指标

请执行这些工具调用。"""
        
        return "我需要调用一些工具来获取必要的数据。"
    
    def _generate_stock_response(self, prompt: str) -> str:
        """生成股票分析响应"""
        stock_name = self._extract_stock_name(prompt)
        
        if not stock_name:
            stock_name = "该股票"
        
        response = f"""根据分析，{stock_name}的情况如下：

**价格走势**
最近一个月{stock_name}呈现震荡上行的态势，整体表现相对稳健。从技术面来看，股价在关键支撑位获得有效支撑。

**技术指标**
- MA5均线与MA10均线形成金叉，短期趋势向好
- MACD指标显示多头动能逐步增强
- RSI指标处于50-70之间，尚未进入超买区域

**基本面**
公司基本面稳健，业绩表现符合市场预期。从估值角度看，当前市盈率处于合理区间。

**投资建议**
综合技术面和基本面分析，{stock_name}当前具有一定的投资价值。建议：
1. 风险承受能力强的投资者可以适当关注
2. 建议分批买入，控制仓位
3. 设置止损位，做好风险控制

*注：以上分析基于历史数据，仅供参考，不构成投资建议。股市有风险，投资需谨慎。*

（这是Mock LLM的模拟响应，实际使用时会由真实的ChatGLM3模型生成）"""
        
        return response
    
    def _generate_general_response(self, prompt: str) -> str:
        """生成通用响应"""
        responses = [
            "这是一个很好的问题。根据我的分析...",
            "让我为您解答这个问题...",
            "基于现有信息，我认为...",
        ]
        
        # 简单的基于长度的选择
        idx = len(prompt) % len(responses)
        prefix = responses[idx]
        
        return f"""{prefix}

根据您的询问，我提供以下信息和建议：

1. **关键要点**：您询问的内容涉及多个方面，需要综合考虑。

2. **详细分析**：从技术角度来看，这个问题有多种解决方案。

3. **建议**：建议您根据实际情况，选择最适合的方案。

（这是Mock LLM的模拟响应，实际使用时会由真实的ChatGLM3模型生成）"""
    
    def _extract_stock_name(self, text: str) -> Optional[str]:
        """从文本中提取股票名称"""
        # 常见股票名称模式
        stock_names = [
            "比亚迪", "宁德时代", "贵州茅台", "中国平安", "招商银行",
            "五粮液", "隆基绿能", "药明康德", "迈瑞医疗", "京东方A",
            "茅台", "平安", "招行"
        ]
        
        for name in stock_names:
            if name in text:
                return name
        
        # 尝试匹配"XXX股票"模式
        match = re.search(r'([^，。、\s]{2,6})(?:股票|的股价|怎么样)', text)
        if match:
            return match.group(1)
        
        return None
    
    def get_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "model_name": "MockLLM",
            "model_type": "mock",
            "version": "1.0",
            "device": "cpu",
            "description": "用于开发和测试的Mock LLM，模拟ChatGLM3行为",
            "call_count": self.call_count,
            "capabilities": [
                "text_generation",
                "stream_generation",
                "stock_analysis",
                "tool_calling"
            ]
        }
    
    async def close(self):
        """关闭模型（Mock版本无需操作）"""
        pass


# 便捷函数
def create_mock_llm(config: Optional[LLMConfig] = None) -> MockLLM:
    """创建Mock LLM实例"""
    if config is None:
        config = LLMConfig(mock_mode=True)
    
    return MockLLM(config)
