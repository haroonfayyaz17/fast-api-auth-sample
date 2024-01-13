import os
from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

print('REDIS_HOST: ', REDIS_HOST)
print('REDIS_PORT: ', REDIS_PORT)


redis_cache = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
