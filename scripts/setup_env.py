"""
环境检查脚本

检查系统环境是否满足运行要求
"""

import sys
import platform
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("   ✅ Python版本满足要求 (>= 3.10)")
        return True
    else:
        print(f"   ❌ Python版本过低，需要 >= 3.10")
        return False

def check_cuda():
    """检查CUDA是否可用"""
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        
        if cuda_available:
            print(f"🎮 CUDA版本: {torch.version.cuda}")
            print(f"   GPU设备: {torch.cuda.get_device_name(0)}")
            
            # 显存信息
            mem_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"   显存大小: {mem_total:.1f} GB")
            
            if mem_total >= 8:
                print("   ✅ 显存满足要求 (>= 8GB)")
                return True
            else:
                print(f"   ⚠️  显存较小 ({mem_total:.1f}GB)，建议使用更小的模型")
                return True
        else:
            print("🎮 CUDA: 不可用")
            print("   ⚠️  未检测到GPU，将使用CPU运行（速度较慢）")
            return True
            
    except ImportError:
        print("🎮 CUDA: 未安装PyTorch")
        print("   ⚠️  请先安装: pip install torch")
        return False

def check_disk_space():
    """检查磁盘空间"""
    project_dir = Path(__file__).parent.parent
    
    try:
        if platform.system() == "Windows":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                str(project_dir), None, None, ctypes.pointer(free_bytes)
            )
            free_gb = free_bytes.value / 1024**3
        else:
            stat = os.statvfs(project_dir)
            free_gb = (stat.f_bavail * stat.f_frsize) / 1024**3
        
        print(f"💾 可用磁盘空间: {free_gb:.1f} GB")
        
        if free_gb >= 20:
            print("   ✅ 磁盘空间充足 (>= 20GB)")
            return True
        else:
            print(f"   ⚠️  磁盘空间不足，建议至少20GB")
            return False
            
    except Exception as e:
        print(f"💾 磁盘空间: 无法检测")
        return True

def check_dependencies():
    """检查关键依赖是否安装"""
    print("\n📦 检查关键依赖:")
    
    dependencies = {
        "torch": "PyTorch",
        "transformers": "Transformers",
        "langchain": "LangChain",
        "fastapi": "FastAPI",
        "chromadb": "ChromaDB",
    }
    
    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} (未安装)")
            all_installed = False
    
    if not all_installed:
        print("\n💡 安装依赖:")
        print("   pip install -r requirements.txt")
    
    return all_installed

def check_model():
    """检查模型是否已下载"""
    model_dir = Path(__file__).parent.parent / "models" / "chatglm3-6b"
    
    if model_dir.exists() and (model_dir / "config.json").exists():
        print(f"\n🤖 模型: 已下载")
        print(f"   📁 {model_dir}")
        return True
    else:
        print(f"\n🤖 模型: 未下载")
        print("   💡 运行: python scripts/download_model.py")
        return False

def check_data():
    """检查数据是否已准备"""
    data_dir = Path(__file__).parent.parent / "data"
    
    stocks_exist = (data_dir / "stocks").exists() and \
                   len(list((data_dir / "stocks").glob("*.parquet"))) > 0
    
    knowledge_exist = (data_dir / "knowledge" / "basics").exists()
    
    vectordb_exist = (data_dir / "vector_db").exists()
    
    print("\n📊 数据状态:")
    print(f"   {'✅' if stocks_exist else '❌'} 股票数据")
    print(f"   {'✅' if knowledge_exist else '❌'} 知识库")
    print(f"   {'✅' if vectordb_exist else '❌'} 向量数据库")
    
    if not stocks_exist:
        print("   💡 运行: python scripts/download_stock_data.py")
    if not vectordb_exist:
        print("   💡 运行: python scripts/build_vectordb.py")
    
    return stocks_exist and knowledge_exist and vectordb_exist

def main():
    """主函数"""
    print()
    print("=" * 60)
    print("🔍 环境检查")
    print("=" * 60)
    print()
    
    checks = [
        ("Python版本", check_python_version()),
        ("CUDA/GPU", check_cuda()),
        ("磁盘空间", check_disk_space()),
    ]
    
    # 如果基础环境OK，检查依赖和数据
    if all(result for _, result in checks):
        checks.append(("依赖包", check_dependencies()))
        checks.append(("模型文件", check_model()))
        checks.append(("数据文件", check_data()))
    
    print()
    print("=" * 60)
    print("📋 检查结果汇总")
    print("=" * 60)
    
    for name, result in checks:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name:15} {status}")
    
    print()
    
    if all(result for _, result in checks):
        print("🎉 环境检查全部通过！可以开始使用系统。")
        print()
        print("🚀 启动服务:")
        print("   python server/start_server.py")
        return 0
    else:
        print("⚠️  部分检查未通过，请根据上述提示修复。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
