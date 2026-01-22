"""
交互式命令行界面

提供友好的用户交互体验
"""

import sys
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from .stock_client import StockClient


class InteractiveCLI:
    """交互式命令行界面"""
    
    def __init__(self, server_url: str = "http://localhost:8765"):
        self.client = StockClient(server_url)
        self.running = False
    
    def print_banner(self):
        """打印欢迎banner"""
        print("\n" + "=" * 70)
        print(" " * 20 + "股票咨询Agent系统")
        print("=" * 70)
        print("\n命令列表:")
        print("  - 直接输入问题进行咨询（如：比亚迪现在多少钱？）")
        print("  - /help  - 显示帮助")
        print("  - /tools - 显示可用工具")
        print("  - /stocks - 显示支持的股票")
        print("  - /quit 或 /exit - 退出")
        print("\n" + "-" * 70)
    
    def print_help(self):
        """打印帮助信息"""
        print("\n帮助信息:")
        print("-" * 70)
        print("\n可以询问的问题类型：")
        print("  1. 价格查询: '比亚迪现在多少钱？'")
        print("  2. 技术分析: '宁德时代的技术指标怎么样？'")
        print("  3. 股票对比: '对比一下比亚迪和宁德时代'")
        print("  4. 知识查询: '什么是MACD指标？'")
        print("  5. 综合分析: '分析一下贵州茅台'")
        print("\n特殊命令：")
        print("  /help   - 显示此帮助")
        print("  /tools  - 查看所有可用工具")
        print("  /stocks - 查看所有支持的股票")
        print("  /quit   - 退出程序")
        print("-" * 70)
    
    def print_tools(self):
        """打印工具列表"""
        print("\n获取工具列表...")
        
        tools = self.client.list_tools()
        
        if tools:
            print("\n可用工具:")
            print("-" * 70)
            
            for i, tool in enumerate(tools, 1):
                print(f"\n{i}. {tool['name']}")
                print(f"   {tool['description']}")
            
            print("-" * 70)
        else:
            print("无法获取工具列表")
    
    def print_stocks(self):
        """打印股票列表"""
        print("\n获取股票列表...")
        
        stocks = self.client.list_stocks()
        
        if stocks:
            print(f"\n支持的股票 (共{len(stocks)}只):")
            print("-" * 70)
            
            # 每行显示3只
            for i in range(0, len(stocks), 3):
                row_stocks = stocks[i:i+3]
                row_text = "  ".join([f"{s['name']}({s['code']})" for s in row_stocks])
                print(f"  {row_text}")
            
            print("-" * 70)
        else:
            print("无法获取股票列表")
    
    def handle_command(self, user_input: str) -> bool:
        """
        处理特殊命令
        
        Args:
            user_input: 用户输入
            
        Returns:
            是否继续运行
        """
        command = user_input.strip().lower()
        
        if command in ['/quit', '/exit', 'quit', 'exit', '退出']:
            return False
        
        elif command in ['/help', 'help', '帮助']:
            self.print_help()
        
        elif command in ['/tools', 'tools', '工具']:
            self.print_tools()
        
        elif command in ['/stocks', 'stocks', '股票']:
            self.print_stocks()
        
        else:
            # 不是命令，是普通查询
            return None
        
        return True
    
    def run(self):
        """运行交互式界面"""
        self.print_banner()
        
        # 检查服务器连接
        print("\n连接服务器...")
        
        if not self.client.health_check():
            print("\n[错误] 无法连接到服务器")
            print("\n请确保服务器已启动:")
            print("  python start_server.py")
            print("\n按Enter退出...")
            input()
            return
        
        print("[OK] 服务器连接成功\n")
        print("=" * 70)
        print("\n开始对话吧！输入 /help 查看帮助\n")
        
        self.running = True
        
        try:
            while self.running:
                # 读取用户输入
                try:
                    user_input = input("您: ").strip()
                except EOFError:
                    break
                
                if not user_input:
                    continue
                
                # 处理命令
                result = self.handle_command(user_input)
                
                if result is False:
                    print("\n再见！")
                    break
                
                elif result is True:
                    # 命令已处理
                    continue
                
                # 普通查询
                print("\n[Agent正在思考...]")
                
                answer = self.client.chat(user_input)
                
                print(f"\nAgent: {answer}\n")
                print("-" * 70)
        
        except KeyboardInterrupt:
            print("\n\n再见！")
        
        finally:
            self.client.close()


def main(server_url: str = "http://localhost:8765"):
    """
    启动交互式CLI
    
    Args:
        server_url: 服务器URL
    """
    cli = InteractiveCLI(server_url)
    cli.run()


if __name__ == "__main__":
    # 支持命令行参数
    import sys
    
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    else:
        server_url = "http://localhost:8765"
    
    main(server_url)
