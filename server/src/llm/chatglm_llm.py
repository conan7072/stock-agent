"""
ChatGLM3 LLM实现

真实的ChatGLM3-6B模型封装
需要GPU环境运行
"""

import asyncio
from typing import AsyncIterator, Optional, Dict, Any
from .base import BaseLLM, LLMConfig


class ChatGLMLLM(BaseLLM):
    """ChatGLM3 LLM - 真实模型"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """加载模型"""
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch
        except ImportError:
            raise ImportError(
                "需要安装transformers和torch: "
                "pip install transformers torch"
            )
        
        print(f"🤖 加载ChatGLM3模型: {self.config.model_path}")
        
        # 加载tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_path,
            trust_remote_code=True
        )
        
        # 加载模型
        self.model = AutoModel.from_pretrained(
            self.config.model_path,
            trust_remote_code=True
        )
        
        # 量化
        if self.config.quantization:
            if self.config.quantization == "int4":
                self.model = self.model.quantize(4)
            elif self.config.quantization == "int8":
                self.model = self.model.quantize(8)
        
        # 移动到设备
        if self.config.device == "cuda":
            self.model = self.model.cuda()
        
        self.model = self.model.eval()
        
        print(f"✅ 模型加载完成")
        print(f"   设备: {self.config.device}")
        print(f"   量化: {self.config.quantization or 'None'}")
    
    async def generate(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """生成响应（非流式）"""
        max_length = max_length or self.config.max_length
        temperature = temperature or self.config.temperature
        
        # 在线程池中运行（避免阻塞事件循环）
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            self._generate_sync,
            prompt,
            max_length,
            temperature
        )
        
        return response
    
    def _generate_sync(
        self,
        prompt: str,
        max_length: int,
        temperature: float
    ) -> str:
        """同步生成"""
        response, _ = self.model.chat(
            self.tokenizer,
            prompt,
            max_length=max_length,
            temperature=temperature,
            top_p=self.config.top_p
        )
        return response
    
    async def generate_stream(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """生成响应（流式）"""
        max_length = max_length or self.config.max_length
        temperature = temperature or self.config.temperature
        
        # ChatGLM3的流式生成
        for response, _ in self.model.stream_chat(
            self.tokenizer,
            prompt,
            max_length=max_length,
            temperature=temperature,
            top_p=self.config.top_p
        ):
            yield response
            await asyncio.sleep(0)  # 让出控制权
    
    def get_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        info = {
            "model_name": self.config.name,
            "model_type": "chatglm3",
            "model_path": self.config.model_path,
            "device": self.config.device,
            "quantization": self.config.quantization,
        }
        
        # 如果在CUDA上，添加显存信息
        if self.config.device == "cuda":
            try:
                import torch
                if torch.cuda.is_available():
                    info["gpu_name"] = torch.cuda.get_device_name(0)
                    info["gpu_memory_allocated"] = f"{torch.cuda.memory_allocated(0) / 1024**3:.2f} GB"
                    info["gpu_memory_reserved"] = f"{torch.cuda.memory_reserved(0) / 1024**3:.2f} GB"
            except:
                pass
        
        return info
    
    async def close(self):
        """关闭模型，释放资源"""
        if self.model is not None:
            del self.model
            self.model = None
        
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        
        # 清理CUDA缓存
        if self.config.device == "cuda":
            try:
                import torch
                torch.cuda.empty_cache()
            except:
                pass


# 便捷函数
def create_chatglm_llm(config: LLMConfig) -> ChatGLMLLM:
    """创建ChatGLM LLM实例"""
    return ChatGLMLLM(config)
