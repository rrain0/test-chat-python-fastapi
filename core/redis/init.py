from fastapi import FastAPI
from redis_fastapi import FastAPIRedis


def init_redis(app: FastAPI):
    FastAPIRedis(app).lifespan().caching()

