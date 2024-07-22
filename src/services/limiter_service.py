from limits.aio.storage import RedisStorage
from limits.aio.strategies import MovingWindowRateLimiter
from settings import settings


storage = RedisStorage(settings.REDIS_CONN_STR)
limiter = MovingWindowRateLimiter(storage)