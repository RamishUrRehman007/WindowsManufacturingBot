import enum
import logging
import os
from typing import List

from arq.connections import RedisSettings


class LOG_LEV(enum.Enum):
    TRACE = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


logger = logging.getLogger(__name__)


def _get_boolean_env_variable(name: str) -> bool:
    return os.getenv(name) == "true"


def _get_comma_separated_env_variable(name: str) -> List[str]:
    return [
        element.strip()
        for element in os.getenv(name, "").split(",")
        if element.strip() != ""
    ]


FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:80")
ROOT_PATH = os.getenv("ROOT_PATH", "")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
VERSION = "1.8.8"
TIMEOUT = 600
LOG_LEVEL = int(os.getenv("LOG_LEVEL", logging.NOTSET))
UVICORN_LOG_LEVEL = "info"
ALLOWED_ORIGINS = _get_comma_separated_env_variable("ALLOWED_ORIGINS")


POSTGRES_URL = os.getenv("POSTGRES_URL", " ")
POSTGRES_MAX_POOL_SIZE = int(os.getenv("POSTGRES_MAX_POOL_SIZE", 100))
DEFAULT_LOCALE = "en_US"


ENVE = "PUSH"
JWT_SECRET = os.getenv("JWT_SECRET", "tS08F4dEaPdAlWjIJEcvDCmDlopBOCXK")
JWT_ISSUER = os.getenv("JWT_ISSUER", "window_manufacturing_bot_user")


REDIS_IP = os.getenv("REDIS_IP", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_SETTINGS = RedisSettings(host=REDIS_IP, port=REDIS_PORT)

ENABLE_RELOAD_UVICORN = _get_boolean_env_variable("ENABLE_RELOAD_UVICORN")



# ====== API KEYS ======
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY", "")
OPEN_AI_MODEL =  os.getenv("OPEN_AI_MODEL", "gpt-3.5-turbo")
