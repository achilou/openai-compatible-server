from typing import Dict, Type, List, Optional, Any
from .base import BaseLLM


class LLMFactory:
    """
    Factory class for managing LLM instances.
    Handles registration and retrieval of LLM implementations.
    """
    
    # Dictionary storing registered LLM classes
    _llm_classes: Dict[str, Type[BaseLLM]] = {}
    
    # Dictionary storing LLM instances (singleton pattern)
    _instances: Dict[str, BaseLLM] = {}
    
    # Default model name
    _default_model: Optional[str] = None
    
    @classmethod
    def register(cls, model_name: str, llm_class: Type[BaseLLM], is_default: bool = False) -> None:
        """
        Register an LLM implementation with the factory.
        
        Args:
            model_name: Unique name for the model
            llm_class: LLM implementation class
            is_default: Whether to set this as the default model
        """
        cls._llm_classes[model_name] = llm_class
        
        # Set as default if specified or no default exists
        if is_default or cls._default_model is None:
            cls._default_model = model_name
    
    @classmethod
    def get_instance(cls, model_name: Optional[str] = None) -> BaseLLM:
        """
        Get an LLM instance by model name.
        
        Args:
            model_name: Name of the model to retrieve. If None, returns default.
            
        Returns:
            LLM instance
            
        Raises:
            ValueError: If model is not found
        """
        # Use default model if none specified
        if model_name is None:
            if cls._default_model is None:
                raise ValueError("No default model registered")
            model_name = cls._default_model
        
        # Create new instance if it doesn't exist
        if model_name not in cls._instances:
            if model_name not in cls._llm_classes:
                raise ValueError(f"Model '{model_name}' not found")
            
            cls._instances[model_name] = cls._llm_classes[model_name]()
        
        return cls._instances[model_name]
    
    @classmethod
    def get_available_models(cls) -> List[Dict[str, Any]]:
        """
        Get list of all available models with their details.
        
        Returns:
            List of model information dictionaries
        """
        models = []
        
        # Get model list from each registered LLM
        for model_name in cls._llm_classes:
            # Create instance if it doesn't exist
            if model_name not in cls._instances:
                cls._instances[model_name] = cls._llm_classes[model_name]()
            
            # Get models supported by this LLM
            llm_models = cls._instances[model_name].get_models()
            models.extend(llm_models)
        
        return models