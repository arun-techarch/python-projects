import os
from .dev import DevConfig
from .prod import ProdConfig

def get_config():
    env = os.getenv("ENV", "dev")  # default = dev
    print(f"env: {env}")
    if env == "prod":
        return ProdConfig()
    return DevConfig()
