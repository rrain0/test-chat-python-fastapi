from fastapi import FastAPI, Depends
from redis_fastapi import cache, AsyncRedisDep, cache_evict

from modules.auth.web.init import init_auth_web
from modules.global_exception_handlers.api_error_case_exception_handler import register_api_error_case_exception_handler
from modules.global_exception_handlers.request_validation_error_handler import register_request_validation_error_handler
from modules.global_openapi_setup.global_openapi_setup import init_openapi
from modules.session.tg_bot.init import init_tg_bot_session
from modules.session.web.init import init_web_session
from core.redis.init import init_redis
from core.postgres.init import init_postgres
from modules.chat.init import init_chat
from modules.msg.init import init_msg

from core.config.env import REDIS_PREFIX
from modules.user.init import init_user



# Create the FastAPI instance
app = FastAPI()

init_redis(app)
init_postgres(app)

register_request_validation_error_handler(app)
register_api_error_case_exception_handler(app)

init_auth_web(app)
init_web_session(app)
init_user(app)
init_tg_bot_session(app)
init_chat(app)
init_msg(app)

init_openapi(app)




# Define a GET route at the root URL
@app.get('/dev/hello-world')
def read_root():
    raise 'Hello World!'
    return {'Hello': 'World'}


# Define a dynamic route with a path parameter
@app.get('/dev/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {'item_id': item_id, 'q': q}



@app.get('/dev/redis-get-set')
async def get_data(redis: AsyncRedisDep):
    """Directly use the Redis client via dependency injection."""
    await redis.set(f'{REDIS_PREFIX}:dev:redis-get-set', 'Hello from Redis SDK', ex=60)
    value = await redis.get(f'{REDIS_PREFIX}:dev:redis-get-set')
    return {'data': value}



# Response is automatically cached
@app.get(
    '/dev/redis-cached-endpoint',
     # Automatically cache the entire HTTP response for 300 seconds.
     dependencies=[Depends(cache(ttl=300, eviction_group='redis-cached-endpoint'))]
)
async def get_cached_endpoint():
    return {'message': 'This response is cached!'}

# Force invalidate cached response
@app.get(
    '/dev/invalidate-redis-cached-endpoint',
     dependencies=[Depends(cache_evict(eviction_group='redis-cached-endpoint'))]
)
async def invalidate_cached_endpoint():
    return {'message': 'Cache group "redis-cached-endpoint" was invalidated!'}

