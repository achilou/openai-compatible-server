import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.llm.factory import LLMFactory
from app.core.llm.mock_llm import MockLLM
from app.api import models, completions, chat_completions
from app.utils.api import create_error_response


# 创建FastAPI应用
app = FastAPI(
    title="OpenAI Compatible Server",
    description="一个兼容OpenAI API的服务器实现",
    version="0.1.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(models.router, prefix=settings.API_V1_STR)
app.include_router(completions.router, prefix=settings.API_V1_STR)
app.include_router(chat_completions.router, prefix=settings.API_V1_STR)


# 注册默认的MockLLM
LLMFactory.register("mock-gpt", MockLLM, is_default=True)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    全局异常处理器
    """
    return create_error_response(
        message=f"服务器内部错误: {str(exc)}",
        type="server_error",
        status_code=500
    )


# 健康检查端点
@app.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "ok"}


if __name__ == "__main__":
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
    )