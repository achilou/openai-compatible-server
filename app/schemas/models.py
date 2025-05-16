from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class ModelPermission(BaseModel):
    """
    模型权限
    """
    id: str
    object: str = "model_permission"
    created: int
    allow_create_engine: bool
    allow_sampling: bool
    allow_logprobs: bool
    allow_search_indices: bool
    allow_view: bool
    allow_fine_tuning: bool
    organization: str
    group: Optional[str] = None
    is_blocking: bool
    
    model_config = ConfigDict(frozen=True)


class Model(BaseModel):
    """
    模型信息
    """
    id: str
    object: str = "model"
    created: int
    owned_by: str
    permission: List[ModelPermission] = []
    root: str
    parent: Optional[str] = None
    
    model_config = ConfigDict(frozen=True)


class ModelList(BaseModel):
    """
    模型列表
    """
    object: str = "list"
    data: List[Model]
    
    model_config = ConfigDict(frozen=True)