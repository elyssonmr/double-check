import aioredis

from double_check import config

redis_cache = aioredis.from_url(config.REDIS_URL)
