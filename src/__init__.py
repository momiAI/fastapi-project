from .config import settings
from .database import *

from src.connectors.redis_maneger import RedisManager
from src.config import settings

redis_manager = RedisManager (
    host = settings.REDIS_HOST,
    port = settings.REDIS_PORT
)