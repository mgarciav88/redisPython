from src.constants import LIST_KEY
from src.redis_client import client, initialize_client, RedisClient


def read_redis_list(redis_client: RedisClient, list_key: str):
    """
    Prints to stdout the elements of a selected redis list
    """
    while redis_client.client.llen(list_key) != 0:
        print(redis_client.client.rpop(list_key))


if __name__ == '__main__':
    initialize_client(client)
    key = LIST_KEY
    read_redis_list(client, key)
