import redis


class RedisClient:
    def __init__(self):
        self.client = None


client = RedisClient()


def initialize_client(redis_client: RedisClient):
    redis_client.client = redis.Redis()
