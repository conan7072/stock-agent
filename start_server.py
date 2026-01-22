"""
启动FastAPI服务器

快速启动股票咨询Agent服务
"""

import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加路径
sys.path.append(str(Path(__file__).parent))

# 导入并运行
from server.src.api.main import main

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("股票咨询Agent服务器")
    print("=" * 60)
    print("\n提示: 按 Ctrl+C 停止服务器\n")
    
    main()
