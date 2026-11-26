from fastapi import FastAPI, Depends
from redis_fastapi import cache, AsyncRedisDep, cache_evict

from modules.auth.web.setup import setup_auth_web
from core.exception_handlers.api_error_case import setup_api_error_case_exception_handler
from core.exception_handlers.request_validation import setup_request_validation_error_handler
from core.openapi.setup import setup_openapi
from modules.session.tg_bot.setup import setup_tg_bot_session
from modules.session.web.setup import setup_web_session
from core.redis.setup import setup_redis
from core.postgres.setup import setup_postgres
from modules.chat.setup import setup_chat
from modules.msg.setup import setup_msg

from modules.user.setup import setup_user



# Create the FastAPI instance
app = FastAPI()

setup_redis(app)
setup_postgres(app)

setup_request_validation_error_handler(app)
setup_api_error_case_exception_handler(app)

setup_auth_web(app)
setup_web_session(app)
setup_user(app)
setup_tg_bot_session(app)
setup_chat(app)
setup_msg(app)

setup_openapi(app)




# Define a GET route at the root URL
@app.get("/dev/hello-world")
def read_root():
    #raise "Hello World!"
    return {"Hello": "World"}


# Define a dynamic route with a path parameter
@app.get("/dev/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}



@app.get("/dev/redis-get-set")
async def get_data(redis: AsyncRedisDep):
    """Directly use the Redis client via dependency injection."""
    await redis.set(f"dev:redis-get-set", "Hello from Redis SDK", ex=60)
    value = await redis.get(f"dev:redis-get-set")
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
    return {"message": "'Cache group 'redis-cached-endpoint' was invalidated!'"}
