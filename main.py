from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from redis_fastapi import cache, AsyncRedisDep, cache_evict

from backend_api_model.back_api_error import BackApiError
from api.routes.tg_user_login_post import tg_user_login_router
from cache.setup.cache_setup import init_fastapi_redis
from db.setup.db_setup import init_db

from api.routes.user_signup_post import user_signup_router
from api.routes.user_login_post import user_login_router
from api.routes.user_current_get import user_current_router
from api.routes.tg_user_msg_post import tg_user_msg_router
from services.env.env import REDIS_PREFIX



# Создаем lifespan-функцию, которая выполнится строго при старте приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()
    yield
    # Shutdown code



# Create the FastAPI instance
app = FastAPI(lifespan=lifespan)


init_fastapi_redis(app)


# Include api routes
app.include_router(user_signup_router)
app.include_router(user_login_router)
app.include_router(tg_user_login_router)
app.include_router(user_current_router)
app.include_router(tg_user_msg_router)



# Перехватываем стандартную ошибку валидации запроса
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            BackApiError(
                error_code="DATA_FORMAT_ERROR",
                msg="Неправильный формат входных данных",
                detail=errors,
            )
        )
    )





# Define a GET route at the root URL
@app.get("/dev/hello-world")
def read_root():
    return {"Hello": "World"}


# Define a dynamic route with a path parameter
@app.get("/dev/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}



@app.get("/dev/redis-get-set")
async def get_data(client: AsyncRedisDep):
    """Directly use the Redis client via dependency injection."""
    await client.set(f"{REDIS_PREFIX}:dev:redis-get-set", "Hello from Redis SDK", ex=60)
    value = await client.get(f"{REDIS_PREFIX}:dev:redis-get-set")
    return {"data": value}



# Response is automatically cached
@app.get(
    "/dev/redis-cached-endpoint",
     # Automatically cache the entire HTTP response for 300 seconds.
     dependencies=[Depends(cache(ttl=300, eviction_group="redis-cached-endpoint"))]
)
async def get_cached_endpoint():
    return {"message": "This response is cached!"}

# Force invalidate cached response
@app.get(
    "/dev/invalidate-redis-cached-endpoint",
     dependencies=[Depends(cache_evict(eviction_group="redis-cached-endpoint"))]
)
async def invalidate_cached_endpoint():
    return {"message": "Cache group 'redis-cached-endpoint' was invalidated!"}

