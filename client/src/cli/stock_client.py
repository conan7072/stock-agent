"""
股票咨询Agent客户端

命令行界面（CLI）客户端
"""

import sys
import requests
from typing import Optional
import json


class StockClient:
    """股票咨询客户端"""
    
    def __init__(self, server_url: str = "http://localhost:8765"):
        self.server_url = server_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """
        健康检查
        
        Returns:
            服务器是否健康
        """
        try:
            response = self.session.get(
                f"{self.server_url}/health",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('status') == 'healthy' and data.get('agent_ready')
            
            return False
        
        except Exception as e:
            return False
    
    def chat(self, query: str) -> Optional[str]:
        """
        发送聊天请求
        
        Args:
            query: 用户查询
            
        Returns:
            Agent回答
        """
        try:
            response = self.session.post(
                f"{self.server_url}/chat",
                json={"query": query},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    return data.get('answer', '')
                else:
                    return f"错误: {data.get('error', '未知错误')}"
            
            else:
                return f"HTTP错误: {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "请求超时，请稍后再试"
        
        except requests.exceptions.ConnectionError:
            return "无法连接到服务器，请确保服务器已启动"
        
        except Exception as e:
            return f"错误: {str(e)}"
    
    def list_tools(self) -> Optional[list]:
        """
        获取工具列表
        
        Returns:
            工具列表
        """
        try:
            response = self.session.get(
                f"{self.server_url}/tools",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('tools', [])
            
            return None
        
        except Exception:
            return None
    
    def list_stocks(self) -> Optional[list]:
        """
        获取股票列表
        
        Returns:
            股票列表
        """
        try:
            response = self.session.get(
                f"{self.server_url}/stocks",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('stocks', [])
            
            return None
        
        except Exception:
            return None
    
    def close(self):
        """关闭连接"""
        self.session.close()
