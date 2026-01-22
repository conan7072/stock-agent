"""
测试LLM功能

验证Mock LLM和真实LLM是否正常工作
"""

import asyncio
import sys
from pathlib import Path

# 设置UTF-8编码（Windows兼容）
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加server/src到路径
sys.path.insert(0, str(Path(__file__).parent / "server" / "src"))

from llm.base import LLMConfig
from llm.factory import create_llm


async def test_mock_llm():
    """测试Mock LLM"""
    print("=" * 60)
    print("[TEST] Mock LLM (无需GPU)")
    print("=" * 60)
    print()
    
    # 创建Mock LLM
    config = LLMConfig(mock_mode=True)
    llm = create_llm(config)
    
    # 显示模型信息
    info = llm.get_info()
    print("[INFO] 模型信息:")
    for key, value in info.items():
        print(f"   {key}: {value}")
    print()
    
    # 测试1: 基础生成
    print("[TEST 1] 基础文本生成")
    print("-" * 60)
    prompt = "你好，请介绍一下你自己"
    print(f"输入: {prompt}")
    print()
    response = await llm.generate(prompt)
    print(f"输出: {response}")
    print()
    
    # 测试2: 股票查询
    print("[TEST 2] 股票分析")
    print("-" * 60)
    prompt = "比亚迪股票最近表现怎么样？"
    print(f"输入: {prompt}")
    print()
    response = await llm.generate(prompt)
    print(f"输出: {response}")
    print()
    
    # 测试3: 流式生成
    print("[TEST 3] 流式生成")
    print("-" * 60)
    prompt = "分析一下宁德时代的投资价值"
    print(f"输入: {prompt}")
    print()
    print("输出: ", end="", flush=True)
    
    async for chunk in llm.generate_stream(prompt):
        print(chunk, end="", flush=True)
    
    print()
    print()
    
    # 关闭
    await llm.close()
    
    print("=" * 60)
    print("[OK] Mock LLM测试完成！")
    print("=" * 60)


async def test_from_config():
    """从配置文件加载LLM"""
    print()
    print("=" * 60)
    print("[TEST] 从配置文件加载")
    print("=" * 60)
    print()
    
    from llm.factory import create_llm_from_config_file
    
    config_path = "server/configs/server_config.yaml"
    
    try:
        llm = create_llm_from_config_file(config_path)
        
        info = llm.get_info()
        print("[INFO] 加载的模型:")
        print(f"   类型: {info.get('model_type')}")
        print(f"   名称: {info.get('model_name')}")
        print()
        
        # 快速测试
        response = await llm.generate("你好")
        print(f"[OK] 生成测试成功")
        print(f"   响应长度: {len(response)} 字符")
        
        await llm.close()
        
    except Exception as e:
        print(f"[ERROR] 加载失败: {e}")


async def main():
    """主函数"""
    print()
    print("=" * 60)
    print("LLM 功能测试")
    print("=" * 60)
    print()
    
    # 测试Mock LLM
    await test_mock_llm()
    
    # 测试配置文件加载
    await test_from_config()
    
    print()
    print("=" * 60)
    print("[SUCCESS] 所有测试完成！")
    print("=" * 60)
    print()
    print("[INFO] 说明:")
    print("   - Mock LLM无需GPU，可在任何机器上运行")
    print("   - 切换到真实模型只需修改 server_config.yaml:")
    print("     model.mock_mode: false")
    print()


if __name__ == "__main__":
    asyncio.run(main())
