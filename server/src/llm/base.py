"""
LLM基础接口

定义统一的LLM接口，支持Mock和真实模型切换
"""

from abc import ABC, abstractmethod
from typing import Optional, AsyncIterator, Dict, Any
from pydantic import BaseModel


class LLMConfig(BaseModel):
    """LLM配置"""
    model_config = {"protected_namespaces": ()}  # 允许model_开头的字段
    
    name: str = "chatglm3-6b"
    model_path: str = "./models/chatglm3-6b"
    device: str = "cuda"  # cuda / cpu
    quantization: Optional[str] = "int4"  # int4 / int8 / fp16 / None
    max_length: int = 4096
    temperature: float = 0.7
    top_p: float = 0.9
    mock_mode: bool = False  # 是否使用Mock模式


class BaseLLM(ABC):
    """LLM基础类"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.model_name = config.name
    
    @abstractmethod
    async def generate(
        self, 
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        生成文本（非流式）
        
        Args:
            prompt: 输入提示词
            max_length: 最大生成长度
            temperature: 温度参数
            
        Returns:
            生成的文本
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        生成文本（流式）
        
        Args:
            prompt: 输入提示词
            max_length: 最大生成长度
            temperature: 温度参数
            
        Yields:
            生成的文本片段
        """
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            包含模型信息的字典
        """
        pass


class LLMResponse(BaseModel):
    """LLM响应"""
    content: str
    model: str
    usage: Optional[Dict[str, int]] = None
    finish_reason: str = "stop"
