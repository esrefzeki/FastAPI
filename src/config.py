import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field, Extra
from FastAPI.src.api.infrastructure.persistance import db_manager

envs_dir = os.path.join(Path(__file__).parent.parent.absolute(), 'envs')


class GlobalConfig(BaseSettings):
    """Global Configuration"""

    ENVIRONMENT: str = Field('dev', env='ENVIRONMENT')

    DB_HOST: Optional[str]
    DB_PASSWORD: Optional[str]
    DB_USERNAME: Optional[str]
    DB_NAME: Optional[str]
    DB_PORT: Optional[str]
    SECRET_KEY: Optional[str]
    ALGORITHM: Optional[str]
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int]

    # SQLALCHEMY_DATABASE_URI: Optional[str]
    # SQLALCHEMY_TRACK_MODIFICATIONS: Optional[bool] = Field(False)


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
#         var = cls.config.SQLALCHEMY_DATABASE_URI
#         return var
