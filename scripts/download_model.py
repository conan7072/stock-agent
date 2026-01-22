"""
模型下载脚本

支持多个模型选择，适配不同显存需求
"""

import os
import sys
import argparse
from pathlib import Path


# 支持的模型配置
MODELS = {
    "chatglm3-6b-int4": {
        "repo": "THUDM/chatglm3-6b",
        "path": "./models/chatglm3-6b",
        "size": "~13GB",
        "vram": "4-5GB",
        "description": "ChatGLM3-6B INT4量化版（推荐RTX 3070）"
    },
    "chatglm3-6b-int8": {
        "repo": "THUDM/chatglm3-6b",
        "path": "./models/chatglm3-6b",
        "size": "~6.5GB",
        "vram": "6-7GB",
        "description": "ChatGLM3-6B INT8量化版"
    },
    "qwen2-7b-int4": {
        "repo": "Qwen/Qwen2-7B-Instruct",
        "path": "./models/qwen2-7b",
        "size": "~14GB",
        "vram": "5-6GB",
        "description": "Qwen2-7B INT4量化版"
    },
    "qwen2-1.5b": {
        "repo": "Qwen/Qwen2-1.5B-Instruct",
        "path": "./models/qwen2-1.5b",
        "size": "~3GB",
        "vram": "2-3GB",
        "description": "Qwen2-1.5B（最快，高并发）"
    }
}


def list_models():
    """列出所有可用模型"""
    print("\n" + "=" * 70)
    print("可用模型列表")
    print("=" * 70 + "\n")
    
    for key, info in MODELS.items():
        print(f"[{key}]")
        print(f"  描述: {info['description']}")
        print(f"  大小: {info['size']}")
        print(f"  显存: {info['vram']}")
        print(f"  仓库: {info['repo']}")
        print()
    
    print("推荐配置:")
    print("  RTX 3070 8GB  -> chatglm3-6b-int4 或 qwen2-1.5b")
    print("  RTX 3060 6GB  -> qwen2-1.5b")
    print("  RTX 4090 24GB -> qwen2-7b-int4")


def download_model(
    model_key: str,
    use_mirror: bool = True
):
    """
    下载模型
    
    Args:
        model_key: 模型键名
        use_mirror: 是否使用镜像
    """
    if model_key not in MODELS:
        print(f"\n错误: 未知模型 '{model_key}'")
        print("\n运行 'python scripts/download_model.py --list' 查看所有模型")
        sys.exit(1)
    
    model_info = MODELS[model_key]
    
    print("=" * 70)
    print("模型下载工具")
    print("=" * 70)
    print()
    
    print(f"模型: {model_key}")
    print(f"描述: {model_info['description']}")
    print(f"文件大小: {model_info['size']}")
    print(f"显存需求: {model_info['vram']}")
    print(f"保存到: {model_info['path']}")
    print()
    
    # 创建目录
    save_dir = Path(model_info['path'])
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # 设置镜像
    if use_mirror:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        print("使用镜像: https://hf-mirror.com")
        print("（国内用户推荐使用镜像加速）")
    
    print()
    
    try:
        from huggingface_hub import snapshot_download
        
        print("开始下载...")
        print("（这可能需要一些时间，取决于网络速度）")
        print()
        
        snapshot_download(
            repo_id=model_info['repo'],
            local_dir=model_info['path'],
            local_dir_use_symlinks=False
        )
        
        print("\n" + "=" * 70)
        print("下载完成！")
        print("=" * 70)
        print(f"\n模型已保存到: {model_info['path']}")
        print("\n下一步：修改配置文件 server/configs/server_config.yaml")
        
        # 提取量化方式
        quant = "int4" if "int4" in model_key else "int8" if "int8" in model_key else "fp16"
        model_name = model_key.split('-')[0]
        
        print(f"""
model:
  mock_mode: false
  name: {model_name}
  path: {model_info['path']}
  device: cuda
  quantization: {quant}
  max_length: 4096
""")
        
    except ImportError:
        print("\n错误: 需要安装 huggingface_hub")
        print("运行: pip install huggingface_hub")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n错误: {str(e)}")
        print("\n如果遇到网络问题:")
        print("  1. 使用镜像: python scripts/download_model.py --model xxx")
        print("  2. 使用代理")
        print("  3. 或手动下载后放到指定目录")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="下载LLM模型（支持多模型选择）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出所有模型
  python scripts/download_model.py --list
  
  # 下载ChatGLM3-6B INT4（推荐RTX 3070 8GB）
  python scripts/download_model.py --model chatglm3-6b-int4
  
  # 下载Qwen2-1.5B（最快，高并发）
  python scripts/download_model.py --model qwen2-1.5b
  
  # 不使用镜像
  python scripts/download_model.py --model chatglm3-6b-int4 --no-mirror
"""
    )
    
    parser.add_argument(
        "--model",
        type=str,
        help="模型名称（如: chatglm3-6b-int4）"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有可用模型"
    )
    
    parser.add_argument(
        "--no-mirror",
        action="store_true",
        help="不使用镜像"
    )
    
    args = parser.parse_args()
    
    # 列出模型
    if args.list:
        list_models()
        return
    
    # 下载模型
    if args.model:
        download_model(
            model_key=args.model,
            use_mirror=not args.no_mirror
        )
    else:
        print("\n请指定模型名称或使用 --list 查看可用模型")
        print("\n示例:")
        print("  python scripts/download_model.py --list")
        print("  python scripts/download_model.py --model chatglm3-6b-int4")


if __name__ == "__main__":
    main()
