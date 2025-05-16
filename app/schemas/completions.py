from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CompletionUsage(BaseModel):
    """
    完成请求的token使用情况
    """
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    model_config = ConfigDict(frozen=True)


class CompletionLogprobs(BaseModel):
    """
    完成请求的logprobs信息
    """
    tokens: List[str]
    token_logprobs: List[float]
    top_logprobs: Optional[List[Dict[str, float]]] = None
    text_offset: List[int]
    
    model_config = ConfigDict(frozen=True)


class CompletionChoice(BaseModel):
    """
    完成请求的单个选择
    """
    text: str
    index: int
    logprobs: Optional[CompletionLogprobs] = None
    finish_reason: Optional[str] = None
    
    model_config = ConfigDict(frozen=True)


class CompletionResponse(BaseModel):
    """
    完成请求的响应
    """
    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: Optional[CompletionUsage] = None
    
    model_config = ConfigDict(frozen=True)


class CompletionRequest(BaseModel):
    """
    完成请求的参数
    """
    model: str
    prompt: Union[str, List[str], List[int], List[List[int]]] = ""
    suffix: Optional[str] = None
    max_tokens: Optional[int] = Field(default=16, ge=1)
    temperature: Optional[float] = Field(default=1.0, ge=0, le=2)
    top_p: Optional[float] = Field(default=1.0, ge=0, le=1)
    n: Optional[int] = Field(default=1, ge=1)
    stream: Optional[bool] = False
    logprobs: Optional[int] = None
    echo: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    frequency_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    best_of: Optional[int] = Field(default=1, ge=1)
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "mock-gpt",
                "prompt": "Hello, world!",
                "max_tokens": 50,
                "temperature": 0.7
            }
        }
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v):
        """验证prompt参数"""
        if isinstance(v, list):
            # 如果是列表，确保所有元素类型一致
            if not v:
                return ""
            if all(isinstance(x, int) for x in v):
                return v
            if all(isinstance(x, list) for x in v):
                if all(all(isinstance(y, int) for y in x) for x in v):
                    return v
            if all(isinstance(x, str) for x in v):
                return v
            raise ValueError("prompt列表元素类型必须一致")
        return v

    @field_validator("best_of")
    @classmethod
    def validate_best_of(cls, v, info):
        """验证best_of参数"""
        if v is not None:
            if v < 1:
                raise ValueError("best_of必须大于等于1")
            if "n" in info.data and info.data["n"] is not None and v < info.data["n"]:
                raise ValueError("best_of必须大于等于n")
        return v