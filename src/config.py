import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field, Extra
from FastAPI.src.api.infrastructure.persistance import db_manager


class GlobalConfig(BaseSettings):

    DB_HOST: str
    DB_PORT: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # SQLALCHEMY_DATABASE_URI: Optional[str]
    # SQLALCHEMY_TRACK_MODIFICATIONS: Optional[bool] = Field(False)

    class Config:
        env_file = ".env"
        # extra = Extra.allow


settings = GlobalConfig()

#
# class DevConfig(GlobalConfig):
#     class Config:
#         env_file: str = os.path.join(envs_dir, 'dev.env')
#
#
# class ProdConfig(GlobalConfig):
#     class Config:
#         env_file: str = os.path.join(envs_dir, 'prod.env')
#
#
# class ConfigManager:
#     config: GlobalConfig
#
#     @classmethod
#     def init_config(cls) -> GlobalConfig:
#         environment = GlobalConfig().ENVIRONMENT
#         if environment == 'dev':
#             cls.config = DevConfig()
#         elif environment == 'prod':
#             cls.config = ProdConfig()
#         else:
#             raise Exception('Environment is not found')
#
#         cls.config.create_db_url()
#         return cls.config
