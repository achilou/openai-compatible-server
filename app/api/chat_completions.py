import logging
from fastapi import APIRouter, HTTPException, status, Request
from typing import List, Dict, Any, Optional
from app.core.llm.factory import LLMFactory
from app.schemas.chat_completions import ChatCompletionRequest, ChatCompletionResponse
from app.utils.api import create_error_response, create_stream_response

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('chat_completions.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'))
logger.addHandler(handler)

router = APIRouter()

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    """
    Handle chat completion requests.
    Supports both streaming and non-streaming responses.
    
    Args:
        request: Chat completion request parameters
        
    Returns:
        ChatCompletionResponse: Chat completion results
    """
    logger.info(f"Received chat completion request for model: {request.model}")
    
    try:
        # Get LLM instance
        llm = LLMFactory.get_instance(request.model)
        
        # Handle streaming response
        if request.stream:
            logger.info("Processing streaming chat completion")
            generator = llm.chat_complete_stream(
                messages=[msg.model_dump() for msg in request.messages],
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                n=request.n,
                stop=request.stop,
                presence_penalty=request.presence_penalty,
                frequency_penalty=request.frequency_penalty,
                logit_bias=request.logit_bias,
                user=request.user,
            )
            return await create_stream_response(generator)
        
        # Handle non-streaming response
        logger.info("Processing non-streaming chat completion")
        response = await llm.chat_complete(
            messages=[msg.model_dump() for msg in request.messages],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            n=request.n,
            stop=request.stop,
            presence_penalty=request.presence_penalty,
            frequency_penalty=request.frequency_penalty,
            logit_bias=request.logit_bias,
            user=request.user,
        )
        
        logger.info("Chat completion request processed successfully")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return create_error_response(
            message=str(e),
            type="invalid_request_error",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return create_error_response(
            message=f"Chat completion request failed: {str(e)}",
            type="server_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )