import json
from typing import Dict, Any, AsyncGenerator, Callable, Awaitable
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse


def create_error_response(
    message: str,
    type: str = "invalid_request_error",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    param: str = None,
    code: str = None,
) -> JSONResponse:
    """
    创建符合OpenAI API错误格式的响应
    
    Args:
        message: 错误消息
        type: 错误类型
        status_code: HTTP状态码
        param: 错误参数
        code: 错误代码
        
    Returns:
        JSONResponse: 错误响应
    """
    error = {
        "message": message,
        "type": type,
    }
    
    if param:
        error["param"] = param
        
    if code:
        error["code"] = code
        
    return JSONResponse(
        status_code=status_code,
        content={"error": error}
    )


async def create_stream_response(
    generator: AsyncGenerator[Dict[str, Any], None],
    content_type: str = "text/event-stream",
) -> StreamingResponse:
    """
    创建流式响应
    
    Args:
        generator: 异步生成器，生成响应数据
        content_type: 内容类型
        
    Returns:
        StreamingResponse: 流式响应
    """
    async def stream_generator():
        try:
            async for chunk in generator:
                yield f"data: {json.dumps(chunk)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_data = {
                "error": {
                    "message": str(e),
                    "type": "server_error",
                }
            }
            yield f"data: {json.dumps(error_data)}\n\n"
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        stream_generator(),
        media_type=content_type,
    )