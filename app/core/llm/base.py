from abc import ABC, abstractmethod
from typing import Dict, List, AsyncGenerator, Optional, Any
from datetime import datetime


class BaseLLM(ABC):
    """
    LLM基类，定义所有LLM实现必须实现的接口
    """
    
    @abstractmethod
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        非流式文本补全
        
        Args:
            prompt: 输入提示文本
            max_tokens: 生成的最大token数
            temperature: 采样温度，控制输出的随机性
            top_p: 核采样参数
            n: 生成多少个补全
            stop: 停止生成的标记列表
            **kwargs: 其他参数
            
        Returns:
            符合OpenAI API格式的响应字典
        """
        pass

    @abstractmethod
    async def complete_stream(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式文本补全
        
        Args:
            prompt: 输入提示文本
            max_tokens: 生成的最大token数
            temperature: 采样温度，控制输出的随机性
            top_p: 核采样参数
            n: 生成多少个补全
            stop: 停止生成的标记列表
            **kwargs: 其他参数
            
        Yields:
            符合OpenAI API格式的响应字典流
        """
        pass

    @abstractmethod
    async def chat_complete(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        非流式聊天补全
        
        Args:
            messages: 对话历史消息列表
            max_tokens: 生成的最大token数
            temperature: 采样温度，控制输出的随机性
            top_p: 核采样参数
            n: 生成多少个补全
            stop: 停止生成的标记列表
            **kwargs: 其他参数
            
        Returns:
            符合OpenAI API格式的响应字典
        """
        pass

    @abstractmethod
    async def chat_complete_stream(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式聊天补全
        
        Args:
            messages: 对话历史消息列表
            max_tokens: 生成的最大token数
            temperature: 采样温度，控制输出的随机性
            top_p: 核采样参数
            n: 生成多少个补全
            stop: 停止生成的标记列表
            **kwargs: 其他参数
            
        Yields:
            符合OpenAI API格式的响应字典流
        """
        pass

    @abstractmethod
    def get_models(self) -> List[Dict[str, Any]]:
        """
        获取当前LLM实现支持的模型列表
        
        Returns:
            模型信息字典列表，每个字典包含模型的详细信息
        """
        pass

    def _get_current_timestamp(self) -> int:
        """
        获取当前Unix时间戳
        
        Returns:
            当前时间戳（秒）
        """
        return int(datetime.now().timestamp())

    def _create_completion_response(
        self,
        text: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        finish_reason: str = "stop",
    ) -> Dict[str, Any]:
        """
        创建标准的completion响应格式
        
        Args:
            text: 生成的文本
            model: 使用的模型名称
            prompt_tokens: 输入提示的token数
            completion_tokens: 生成文本的token数
            finish_reason: 生成停止的原因
            
        Returns:
            标准格式的completion响应字典
        """
        return {
            "id": f"cmpl-{self._get_current_timestamp()}",
            "object": "text_completion",
            "created": self._get_current_timestamp(),
            "model": model,
            "choices": [
                {
                    "text": text,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": finish_reason
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        }

    def _create_chat_completion_response(
        self,
        content: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        finish_reason: str = "stop",
        role: str = "assistant",
    ) -> Dict[str, Any]:
        """
        创建标准的chat completion响应格式
        
        Args:
            content: 生成的内容
            model: 使用的模型名称
            prompt_tokens: 输入提示的token数
            completion_tokens: 生成内容的token数
            finish_reason: 生成停止的原因
            role: 响应角色
            
        Returns:
            标准格式的chat completion响应字典
        """
        return {
            "id": f"chatcmpl-{self._get_current_timestamp()}",
            "object": "chat.completion",
            "created": self._get_current_timestamp(),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": role,
                        "content": content
                    },
                    "finish_reason": finish_reason
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        }