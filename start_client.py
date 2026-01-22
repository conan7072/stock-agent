"""
启动CLI客户端

快速启动股票咨询客户端
"""

import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加路径
sys.path.append(str(Path(__file__).parent))

from client.src.cli.interactive import main

if __name__ == "__main__":
    # 默认服务器地址
    server_url = "http://localhost:8765"
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    
    main(server_url)
