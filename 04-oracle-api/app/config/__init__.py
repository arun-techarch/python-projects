import os
import logging
from .dev import DevConfig
from .prod import ProdConfig

logger = logging.getLogger(__name__)

def get_config():
    env = os.getenv("ENV", "dev")  # default = dev
    logger.info(f"env: {env}")
    if env == "prod":
        return ProdConfig()
    return DevConfig()
