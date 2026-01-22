"""
FastAPI服务主入口

提供股票咨询Agent的HTTP API接口
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, AsyncIterator
import asyncio
import sys
from pathlib import Path
import yaml

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from server.src.agent.stock_agent import get_agent
from server.src.llm.factory import create_llm_from_config_file


# ==================== 配置 ====================

CONFIG_PATH = "./server/configs/server_config.yaml"

# 加载配置
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    server_config = yaml.safe_load(f)

SERVER_HOST = server_config.get('server', {}).get('host', '0.0.0.0')
SERVER_PORT = server_config.get('server', {}).get('port', 8765)


# ==================== FastAPI应用 ====================

app = FastAPI(
    title="股票咨询Agent API",
    description="基于LLM的股票咨询智能Agent服务",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 请求/响应模型 ====================

class QueryRequest(BaseModel):
    """查询请求"""
    query: str
    stream: bool = False  # 是否流式响应


class QueryResponse(BaseModel):
    """查询响应"""
    answer: str
    success: bool = True
    error: Optional[str] = None


# ==================== 全局变量 ====================

agent = None


# ==================== 生命周期 ====================

@app.on_event("startup")
async def startup_event():
    """启动时初始化Agent"""
    global agent
    
    print("=" * 60)
    print("启动股票咨询Agent服务...")
    print("=" * 60)
    
    # 初始化Agent
    agent = get_agent(CONFIG_PATH)
    
    print(f"\n服务已启动:")
    print(f"  - Host: {SERVER_HOST}")
    print(f"  - Port: {SERVER_PORT}")
    print(f"  - API Docs: http://{SERVER_HOST}:{SERVER_PORT}/docs")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理资源"""
    print("\n关闭服务...")


# ==================== API端点 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "股票咨询Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "agent_ready": agent is not None
    }


@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """
    聊天接口（非流式）
    
    Args:
        request: 查询请求
        
    Returns:
        查询响应
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent未初始化")
    
    try:
        # 调用Agent
        answer = agent.chat(request.query)
        
        return QueryResponse(
            answer=answer,
            success=True
        )
    
    except Exception as e:
        return QueryResponse(
            answer="",
            success=False,
            error=str(e)
        )


@app.post("/chat/stream")
async def chat_stream(request: QueryRequest):
    """
    聊天接口（流式）
    
    Args:
        request: 查询请求
        
    Returns:
        流式响应
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent未初始化")
    
    async def generate_stream() -> AsyncIterator[str]:
        """生成流式响应"""
        try:
            # 获取答案
            answer = agent.chat(request.query)
            
            # 模拟流式输出（每次输出几个字符）
            chunk_size = 10
            for i in range(0, len(answer), chunk_size):
                chunk = answer[i:i+chunk_size]
                yield f"data: {chunk}\n\n"
                await asyncio.sleep(0.05)  # 模拟延迟
            
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: [ERROR: {str(e)}]\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )


@app.get("/tools")
async def list_tools():
    """列出所有可用工具"""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent未初始化")
    
    tools_info = []
    
    for tool_name, tool in agent.tools.items():
        tools_info.append({
            "name": tool_name,
            "description": tool.description
        })
    
    return {
        "tools": tools_info,
        "count": len(tools_info)
    }


@app.get("/stocks")
async def list_stocks():
    """列出所有支持的股票"""
    from server.src.data.stock_loader import get_loader
    
    loader = get_loader()
    stocks = loader.list_available_stocks()
    
    return {
        "stocks": stocks,
        "count": len(stocks)
    }


# ==================== 错误处理 ====================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "detail": "服务器内部错误"
        }
    )


# ==================== 主函数 ====================

def main():
    """运行服务器"""
    import uvicorn
    
    uvicorn.run(
        "server.src.api.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
