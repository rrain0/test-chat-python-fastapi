from fastapi import FastAPI
from redis_fastapi import FastAPIRedis


def init_fastapi_redis(app: FastAPI):
    FastAPIRedis(app).lifespan().caching()

