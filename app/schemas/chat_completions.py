from typing import List, Optional, Union, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

from .completions import CompletionUsage


class ChatCompletionMessage(BaseModel):
    """
    聊天消息
    """
    role: str
    content: str
    name: Optional[str] = None

    model_config = ConfigDict(frozen=True)

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        """验证role参数"""
        allowed_roles = {"system", "user", "assistant", "function"}
        if v not in allowed_roles:
            raise ValueError(f"role必须是以下之一: {allowed_roles}")
        return v


class ChatCompletionChoice(BaseModel):
    """
    聊天完成请求的单个选择
    """
    index: int
    message: ChatCompletionMessage
    finish_reason: Optional[str] = None
    
    model_config = ConfigDict(frozen=True)


class ChatCompletionResponse(BaseModel):
    """
    聊天完成请求的响应
    """
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[CompletionUsage] = None
    
    model_config = ConfigDict(frozen=True)


class ChatCompletionRequest(BaseModel):
    """
    聊天完成请求的参数
    """
    model: str
    messages: List[ChatCompletionMessage]
    temperature: Optional[float] = Field(default=1.0, ge=0, le=2)
    top_p: Optional[float] = Field(default=1.0, ge=0, le=1)
    n: Optional[int] = Field(default=1, ge=1)
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = Field(default=None, ge=1)
    presence_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    frequency_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "mock-gpt",
                "messages": [
                    {"role": "user", "content": "Hello, how are you?"}
                ],
                "temperature": 0.7
            }
        }
    )

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v):
        """验证messages参数"""
        if not v:
            raise ValueError("messages不能为空")
        return v


class ChatCompletionChunkDelta(BaseModel):
    """
    聊天完成流式响应的增量内容
    """
    role: Optional[str] = None
    content: Optional[str] = None
    
    model_config = ConfigDict(frozen=True)


class ChatCompletionChunkChoice(BaseModel):
    """
    聊天完成流式响应的单个选择
    """
    index: int
    delta: ChatCompletionChunkDelta
    finish_reason: Optional[str] = None
    
    model_config = ConfigDict(frozen=True)


class ChatCompletionChunk(BaseModel):
    """
    聊天完成流式响应
    """
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionChunkChoice]
    usage: Optional[CompletionUsage] = None
    
    model_config = ConfigDict(frozen=True)