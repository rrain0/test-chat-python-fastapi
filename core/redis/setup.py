from fastapi import FastAPI
from redis_fastapi import FastAPIRedis


def setup_redis(app: FastAPI):
    FastAPIRedis(app).lifespan().caching()

