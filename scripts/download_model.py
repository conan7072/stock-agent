"""
模型下载脚本

支持多个模型选择，适配不同显存需求
"""

import os
import sys
import argparse
import time
from pathlib import Path

# 设置UTF-8编码（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


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


def print_separator(char="=", length=70):
    """打印分隔线"""
    print(char * length)


def print_step(step_num, total_steps, message):
    """打印步骤信息"""
    print(f"\n[步骤 {step_num}/{total_steps}] {message}")
    print("-" * 70)


def check_dependencies():
    """检查依赖"""
    print_step(1, 5, "检查依赖...")
    
    try:
        import huggingface_hub
        print("✓ huggingface_hub 已安装")
        return True
    except ImportError:
        print("✗ huggingface_hub 未安装")
        print("\n请先安装依赖:")
        print("  pip install huggingface_hub")
        print("\n或安装完整依赖:")
        print("  pip install -r requirements.txt")
        return False


def check_disk_space(required_gb):
    """检查磁盘空间"""
    print_step(2, 5, "检查磁盘空间...")
    
    try:
        import shutil
        stat = shutil.disk_usage('.')
        free_gb = stat.free / (1024**3)
        
        print(f"当前目录可用空间: {free_gb:.1f} GB")
        print(f"模型大小约: {required_gb} GB")
        
        if free_gb < required_gb * 1.5:
            print(f"\n⚠️ 警告: 磁盘空间可能不足")
            print(f"建议至少有 {required_gb * 1.5:.0f} GB 可用空间")
            response = input("\n是否继续? [y/N]: ").strip().lower()
            return response == 'y'
        else:
            print("✓ 磁盘空间充足")
            return True
            
    except Exception as e:
        print(f"无法检查磁盘空间: {e}")
        print("继续下载...")
        return True


def check_existing_files(model_path):
    """检查是否已存在模型文件"""
    print_step(3, 5, "检查现有文件...")
    
    model_dir = Path(model_path)
    if model_dir.exists():
        files = list(model_dir.glob('*'))
        if files:
            print(f"✓ 发现现有文件 {len(files)} 个")
            print(f"路径: {model_dir}")
            print("\n选项:")
            print("  1. 继续下载（断点续传）")
            print("  2. 删除重新下载")
            print("  3. 取消")
            
            choice = input("\n请选择 [1/2/3]: ").strip()
            
            if choice == '2':
                print("\n正在删除现有文件...")
                import shutil
                shutil.rmtree(model_dir)
                print("✓ 已删除")
                model_dir.mkdir(parents=True, exist_ok=True)
            elif choice == '3':
                print("\n已取消")
                return False
            # choice == '1' 继续
        else:
            print("✓ 目录为空，准备下载")
    else:
        print("✓ 创建目录: " + str(model_dir))
        model_dir.mkdir(parents=True, exist_ok=True)
    
    return True


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


class DownloadProgress:
    """下载进度显示"""
    def __init__(self):
        self.start_time = time.time()
        self.last_print_time = self.start_time
        self.file_count = 0
        
    def __call__(self, block_num, block_size, total_size):
        """进度回调"""
        if total_size > 0:
            downloaded = block_num * block_size
            percent = min(100, downloaded * 100 / total_size)
            
            # 每秒更新一次
            current_time = time.time()
            if current_time - self.last_print_time >= 1.0:
                elapsed = current_time - self.start_time
                speed = downloaded / elapsed / (1024 * 1024)  # MB/s
                
                print(f"\r下载进度: {percent:.1f}% | "
                      f"已下载: {downloaded/(1024**2):.1f}MB / {total_size/(1024**2):.1f}MB | "
                      f"速度: {speed:.2f} MB/s", end='', flush=True)
                
                self.last_print_time = current_time


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
        print(f"\n✗ 错误: 未知模型 '{model_key}'")
        print("\n运行以下命令查看所有模型:")
        print("  python scripts/download_model.py --list")
        sys.exit(1)
    
    model_info = MODELS[model_key]
    
    # 显示标题
    print("\n" + "=" * 70)
    print(f"模型下载工具 - {model_key}")
    print("=" * 70)
    print()
    
    print(f"模型: {model_key}")
    print(f"描述: {model_info['description']}")
    print(f"文件大小: {model_info['size']}")
    print(f"显存需求: {model_info['vram']}")
    print(f"保存路径: {model_info['path']}")
    print(f"Hugging Face: {model_info['repo']}")
    print()
    
    # 步骤1: 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 步骤2: 检查磁盘空间
    required_size = int(model_info['size'].replace('~', '').replace('GB', ''))
    if not check_disk_space(required_size):
        print("\n已取消下载")
        sys.exit(0)
    
    # 步骤3: 检查现有文件
    if not check_existing_files(model_info['path']):
        sys.exit(0)
    
    # 步骤4: 配置下载
    print_step(4, 5, "配置下载...")
    
    if use_mirror:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        print("✓ 使用镜像: https://hf-mirror.com (国内推荐)")
    else:
        print("✓ 使用官方源: https://huggingface.co")
    
    # 步骤5: 开始下载
    print_step(5, 5, "开始下载...")
    print()
    print("提示:")
    print("  - 下载时间取决于网络速度")
    print("  - 可以按 Ctrl+C 中断，下次会断点续传")
    print("  - 请保持网络连接稳定")
    print()
    
    start_time = time.time()
    
    try:
        from huggingface_hub import snapshot_download
        
        print("正在从 Hugging Face 下载...")
        print(f"仓库: {model_info['repo']}")
        print()
        
        # 下载模型
        snapshot_download(
            repo_id=model_info['repo'],
            local_dir=model_info['path'],
            local_dir_use_symlinks=False,
            resume_download=True,  # 支持断点续传
        )
        
        elapsed = time.time() - start_time
        
        # 成功
        print("\n")
        print_separator("=")
        print("✓ 下载完成！")
        print_separator("=")
        print()
        print(f"耗时: {elapsed/60:.1f} 分钟")
        print(f"路径: {model_info['path']}")
        print()
        
        # 显示下一步
        print("下一步操作:")
        print()
        print("1. 修改配置文件:")
        print("   编辑 server/configs/server_config.yaml")
        print()
        print("2. 设置以下配置:")
        
        quant = "int4" if "int4" in model_key else "int8" if "int8" in model_key else "fp16"
        model_name = model_key.split('-')[0]
        
        print()
        print("   model:")
        print("     mock_mode: false")
        print(f"     name: {model_name}")
        print(f"     path: {model_info['path']}")
        print("     device: cuda")
        print(f"     quantization: {quant}")
        print("     max_length: 4096")
        print()
        
        print("3. 启动服务:")
        print("   python start_server.py")
        print()
        
        return True
        
    except KeyboardInterrupt:
        print("\n")
        print("=" * 70)
        print("⚠️  下载已中断")
        print("=" * 70)
        print()
        print("提示: 下次运行此脚本会自动从断点继续")
        print()
        return False
        
    except ImportError as e:
        print("\n")
        print("=" * 70)
        print("✗ 依赖错误")
        print("=" * 70)
        print()
        print(f"错误: {str(e)}")
        print()
        print("解决方法:")
        print("  pip install huggingface_hub")
        print()
        return False
        
    except Exception as e:
        print("\n")
        print("=" * 70)
        print("✗ 下载失败")
        print("=" * 70)
        print()
        print(f"错误: {str(e)}")
        print()
        print("可能的原因:")
        print("  1. 网络连接问题")
        print("  2. Hugging Face 服务不可用")
        print("  3. 磁盘空间不足")
        print()
        print("解决方法:")
        print("  1. 检查网络连接")
        print("  2. 使用镜像: python scripts/download_model.py --model xxx")
        print("  3. 使用代理/VPN")
        print("  4. 稍后重试（支持断点续传）")
        print()
        print("手动下载:")
        print(f"  访问: https://huggingface.co/{model_info['repo']}")
        print(f"  下载到: {model_info['path']}")
        print()
        return False


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
        success = download_model(
            model_key=args.model,
            use_mirror=not args.no_mirror
        )
        sys.exit(0 if success else 1)
    else:
        print("\n请指定模型名称或使用 --list 查看可用模型")
        print("\n示例:")
        print("  python scripts/download_model.py --list")
        print("  python scripts/download_model.py --model chatglm3-6b-int4")
        print()


if __name__ == "__main__":
    main()
