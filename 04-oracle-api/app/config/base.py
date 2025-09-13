from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    app_name: str = "My FastAPI App"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
