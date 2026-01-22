"""
LLM工厂

根据配置自动创建Mock或真实LLM
"""

from typing import Optional
from .base import BaseLLM, LLMConfig
from .mock_llm import MockLLM
from .chatglm_llm import ChatGLMLLM


def create_llm(config: Optional[LLMConfig] = None) -> BaseLLM:
    """
    创建LLM实例
    
    根据配置自动选择Mock LLM或真实LLM
    
    Args:
        config: LLM配置，如果为None则使用默认配置
        
    Returns:
        LLM实例
    """
    if config is None:
        config = LLMConfig()
    
    # 检查是否使用Mock模式
    if config.mock_mode:
        print("🎭 使用Mock LLM（无需GPU）")
        return MockLLM(config)
    
    # 检查是否有GPU
    try:
        import torch
        has_cuda = torch.cuda.is_available()
        
        if config.device == "cuda" and not has_cuda:
            print("⚠️  未检测到CUDA，自动切换到Mock模式")
            config.mock_mode = True
            return MockLLM(config)
    except ImportError:
        print("⚠️  未安装PyTorch，自动切换到Mock模式")
        config.mock_mode = True
        return MockLLM(config)
    
    # 使用真实模型
    print(f"🤖 使用真实LLM: {config.name}")
    
    if "chatglm" in config.name.lower():
        return ChatGLMLLM(config)
    else:
        raise ValueError(f"不支持的模型: {config.name}")


def create_llm_from_config_file(config_path: str) -> BaseLLM:
    """
    从配置文件创建LLM
    
    Args:
        config_path: 配置文件路径（YAML）
        
    Returns:
        LLM实例
    """
    import yaml
    from pathlib import Path
    
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config_dict = yaml.safe_load(f)
    
    # 提取model配置
    model_config = config_dict.get('model', {})
    
    # 创建LLMConfig
    llm_config = LLMConfig(
        name=model_config.get('name', 'chatglm3-6b'),
        model_path=model_config.get('path', './models/chatglm3-6b'),
        device=model_config.get('device', 'cuda'),
        quantization=model_config.get('quantization', 'int4'),
        max_length=model_config.get('max_length', 4096),
        temperature=model_config.get('temperature', 0.7),
        top_p=model_config.get('top_p', 0.9),
        mock_mode=model_config.get('mock_mode', False)
    )
    
    return create_llm(llm_config)


# 全局LLM实例（单例模式）
_global_llm: Optional[BaseLLM] = None


def get_llm() -> BaseLLM:
    """
    获取全局LLM实例
    
    如果还未初始化，则使用默认配置创建
    
    Returns:
        LLM实例
    """
    global _global_llm
    
    if _global_llm is None:
        _global_llm = create_llm()
    
    return _global_llm


def set_llm(llm: BaseLLM):
    """
    设置全局LLM实例
    
    Args:
        llm: LLM实例
    """
    global _global_llm
    _global_llm = llm


async def close_llm():
    """关闭全局LLM实例"""
    global _global_llm
    
    if _global_llm is not None:
        await _global_llm.close()
        _global_llm = None
