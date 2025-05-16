import logging
from fastapi import APIRouter, HTTPException, status, Request
from typing import List, Dict, Any, Optional, Union
from app.core.llm.factory import LLMFactory
from app.schemas.completions import CompletionRequest, CompletionResponse
from app.utils.api import create_error_response, create_stream_response

# Configure logger for completions endpoint
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('completions.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'))
logger.addHandler(handler)

router = APIRouter()

@router.post("/completions", response_model=CompletionResponse)
async def create_completion(request: CompletionRequest):
    """
    Handle text completion requests including both streaming and non-streaming modes.
    
    Args:
        request: Completion request containing:
            - model: The LLM model to use
            - prompt: Input text or token sequence
            - stream: Whether to stream the response
            - Other completion parameters
        
    Returns:
        Completion response in OpenAI API format
        OR
        StreamingResponse for streaming mode
        
    Raises:
        HTTPException: For invalid requests or server errors
    """
    logger.info(f"Processing completion request for model: {request.model}")
    
    try:
        # Get the appropriate LLM instance
        llm = LLMFactory.get_instance(request.model)
        
        # Process prompt parameter (handle both string and token list formats)
        prompt = request.prompt
        if isinstance(prompt, list):
            if all(isinstance(x, str) for x in prompt):
                # Use first element if it's a string list
                prompt = prompt[0] if prompt else ""
            else:
                logger.warning("Token list prompts are not supported")
                return create_error_response(
                    message="Token lists as prompts are not supported",
                    type="invalid_request_error",
                    param="prompt"
                )
        
        # Handle streaming response
        if request.stream:
            logger.info("Generating streaming completion response")
            generator = llm.complete_stream(
                prompt=prompt,
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
        
        # Handle standard non-streaming response
        logger.info("Generating standard completion response")
        response = await llm.complete(
            prompt=prompt,
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
        
        logger.info("Successfully generated completion response")
        return response
        
    except ValueError as e:
        logger.error(f"Invalid request parameters: {str(e)}")
        return create_error_response(
            message=str(e),
            type="invalid_request_error",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Completion processing failed: {str(e)}")
        return create_error_response(
            message=f"Completion request failed: {str(e)}",
            type="server_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )