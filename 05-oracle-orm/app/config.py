import logging
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    ORACLE_USER:str
    ORACLE_PASSWORD:str
    ORACLE_HOST:str = "localhost"
    ORACLE_PORT:int = 1521
    ORACLE_SERVICE:str = "FREE"
    SQL_ECHO:bool = False

    class Config:
        env_file = ".env"
        logger.info("Loaded the configuration")

settings = Settings()