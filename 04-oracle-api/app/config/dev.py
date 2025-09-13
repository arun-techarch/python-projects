from .base import BaseConfig

class DevConfig(BaseConfig):
    debug: bool = True
    oracle_dsn: str = "localhost:1521/FREE"
    oracle_user: str = "SYSTEM"
    oracle_password: str = "Admin@123"
