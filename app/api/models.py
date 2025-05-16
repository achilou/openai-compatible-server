import logging
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.core.llm.factory import LLMFactory
from app.schemas.models import ModelList, Model
from app.utils.api import create_error_response

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('models.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'))
logger.addHandler(handler)

router = APIRouter()

@router.get("/models", response_model=ModelList)
async def list_models():
    """
    Retrieve list of all available models.
    
    Returns:
        ModelList: Contains list of available models
    """
    logger.info("Listing all available models")
    try:
        models = LLMFactory.get_available_models()
        logger.info(f"Found {len(models)} models")
        return {"object": "list", "data": models}
    except Exception as e:
        logger.error(f"Failed to list models: {str(e)}")
        return create_error_response(
            message=f"Failed to retrieve model list: {str(e)}",
            type="server_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/models/{model_id}", response_model=Model)
async def get_model(model_id: str):
    """
    Retrieve details for a specific model.
    
    Args:
        model_id: ID of the model to retrieve
        
    Returns:
        Model: Detailed information about the requested model
    """
    logger.info(f"Getting details for model: {model_id}")
    try:
        models = LLMFactory.get_available_models()
        for model in models:
            if model.get("id") == model_id:
                logger.info(f"Found model: {model_id}")
                return model
                
        logger.warning(f"Model not found: {model_id}")
        return create_error_response(
            message=f"Model '{model_id}' not found",
            type="invalid_request_error",
            param="model",
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Failed to get model details: {str(e)}")
        return create_error_response(
            message=f"Failed to retrieve model information: {str(e)}",
            type="server_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )