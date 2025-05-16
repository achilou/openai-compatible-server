from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    应用配置
    """
    # API配置
    API_V1_STR: str = "/v1"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS配置
    CORS_ORIGINS: str = "*"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局设置实例
settings = Settings()