from .base import BaseConfig

class ProdConfig(BaseConfig):
    oracle_dsn: str = "localhost:1522/FREE"
    oracle_user: str = "SYSTEM"
    oracle_password: str = "Admin@456"
