import asyncio
import random
from typing import Dict, List, AsyncGenerator, Optional, Any
from datetime import datetime

from .base import BaseLLM


class MockLLM(BaseLLM):
    """
    Mock LLM implementation for testing and demonstration purposes.
    Provides simulated responses for all required interfaces.
    """
    
    def __init__(self):
        """Initialize mock LLM with default model names"""
        self.model_name = "mock-gpt"
        self.model_id = "mock-gpt-1"
        
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
        Simulate non-streaming text completion.
        
        Args:
            prompt: Input prompt text
            max_tokens: Maximum tokens to generate (ignored)
            temperature: Sampling temperature (ignored)
            top_p: Nucleus sampling parameter (ignored)
            n: Number of completions (ignored, always 1)
            stop: Stop sequences (ignored)
            **kwargs: Additional parameters (ignored)
            
        Returns:
            Simulated completion response
        """
        # Simulate processing delay
        await asyncio.sleep(0.5)
        
        # Generate mock response
        response_text = f"This is a mock response to: {prompt}"
        
        # Calculate token counts (simplified)
        prompt_tokens = len(prompt.split())
        completion_tokens = len(response_text.split())
        
        return self._create_completion_response(
            text=response_text,
            model=self.model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens
        )

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
        Simulate streaming text completion.
        
        Args:
            prompt: Input prompt text
            max_tokens: Maximum tokens to generate (ignored)
            temperature: Sampling temperature (ignored)
            top_p: Nucleus sampling parameter (ignored)
            n: Number of completions (ignored, always 1)
            stop: Stop sequences (ignored)
            **kwargs: Additional parameters (ignored)
            
        Yields:
            Simulated streaming response chunks
        """
        # Generate mock response
        response_text = f"This is a mock response to: {prompt}"
        words = response_text.split()
        
        # Create unique ID for this completion
        completion_id = f"cmpl-{self._get_current_timestamp()}"
        created = self._get_current_timestamp()
        
        # Calculate prompt tokens (simplified)
        prompt_tokens = len(prompt.split())
        
        # Yield response word by word
        for i, word in enumerate(words):
            # Simulate processing delay
            await asyncio.sleep(0.1)
            
            is_last = i == len(words) - 1
            finish_reason = "stop" if is_last else None
            
            yield {
                "id": completion_id,
                "object": "text_completion",
                "created": created,
                "model": self.model_name,
                "choices": [
                    {
                        "text": word + " ",
                        "index": 0,
                        "logprobs": None,
                        "finish_reason": finish_reason
                    }
                ]
            }
            
        # Final chunk with usage info
        completion_tokens = len(words)
        yield {
            "id": completion_id,
            "object": "text_completion",
            "created": created,
            "model": self.model_name,
            "choices": [
                {
                    "text": "",
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        }

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
        Simulate non-streaming chat completion.
        
        Args:
            messages: Conversation history
            max_tokens: Maximum tokens to generate (ignored)
            temperature: Sampling temperature (ignored)
            top_p: Nucleus sampling parameter (ignored)
            n: Number of completions (ignored, always 1)
            stop: Stop sequences (ignored)
            **kwargs: Additional parameters (ignored)
            
        Returns:
            Simulated chat completion response
        """
        # Simulate processing delay
        await asyncio.sleep(0.5)
        
        # Get last user message
        last_message = messages[-1] if messages else {"role": "user", "content": ""}
        
        # Generate mock response
        if last_message["role"] == "user":
            response_content = f"This is a mock chat response to: {last_message['content']}"
        else:
            response_content = "I'm a mock AI assistant. How can I help you today?"
        
        # Calculate token counts (simplified)
        prompt_tokens = sum(len(msg.get("content", "").split()) for msg in messages)
        completion_tokens = len(response_content.split())
        
        return self._create_chat_completion_response(
            content=response_content,
            model=self.model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens
        )

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
        Simulate streaming chat completion.
        
        Args:
            messages: Conversation history
            max_tokens: Maximum tokens to generate (ignored)
            temperature: Sampling temperature (ignored)
            top_p: Nucleus sampling parameter (ignored)
            n: Number of completions (ignored, always 1)
            stop: Stop sequences (ignored)
            **kwargs: Additional parameters (ignored)
            
        Yields:
            Simulated streaming chat completion chunks
        """
        # Get last user message
        last_message = messages[-1] if messages else {"role": "user", "content": ""}
        
        # Generate mock response
        if last_message["role"] == "user":
            response_content = f"This is a mock chat response to: {last_message['content']}"
        else:
            response_content = "I'm a mock AI assistant. How can I help you today?"
            
        words = response_content.split()
        
        # Create unique ID for this completion
        completion_id = f"chatcmpl-{self._get_current_timestamp()}"
        created = self._get_current_timestamp()
        
        # Calculate prompt tokens (simplified)
        prompt_tokens = sum(len(msg.get("content", "").split()) for msg in messages)
        
        # Initial chunk with role
        yield {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": self.model_name,
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "role": "assistant"
                    },
                    "finish_reason": None
                }
            ]
        }
        
        # Yield response word by word
        for i, word in enumerate(words):
            # Simulate processing delay
            await asyncio.sleep(0.1)
            
            is_last = i == len(words) - 1
            finish_reason = "stop" if is_last else None
            
            yield {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": self.model_name,
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "content": word + " "
                        },
                        "finish_reason": finish_reason
                    }
                ]
            }
        
        # Final chunk with usage info
        completion_tokens = len(words)
        yield {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": self.model_name,
            "choices": [
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        }

    def get_models(self) -> List[Dict[str, Any]]:
        """
        Get list of models supported by this mock implementation.
        
        Returns:
            List containing mock model information
        """
        return [
            {
                "id": self.model_id,
                "object": "model",
                "created": int(datetime(2023, 1, 1).timestamp()),
                "owned_by": "mock-organization",
                "permission": [],
                "root": self.model_id,
                "parent": None
            }
        ]