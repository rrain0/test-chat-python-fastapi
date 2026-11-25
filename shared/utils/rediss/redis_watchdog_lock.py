import asyncio
import contextlib
import logging

from redis_fastapi import AsyncRedisDep

logger = logging.getLogger(__name__)

class RedisLockLostError(Exception):
    """Raised when the background watchdog fails to extend the Redis lock."""
    pass



@contextlib.asynccontextmanager
async def redis_watchdog_lock(
    redis: AsyncRedisDep,
    key: str,
    acquire_timeout: float = 6.0,
    renew_interval: float = 1.0,
    timeout: float = 3.0,
):
    key = f'lock:{key}'
    owner_task = asyncio.current_task()
    failed_to_extend_lock = False
    extend_error: Exception | None = None

    lock = redis.lock(
        name=key,

        sleep=0.2, # interval to check lock while trying to acquire lock
        blocking=True, # wait for lock to be available or time runs out while trying to acquire lock
        blocking_timeout=acquire_timeout, # maximum amount of time to wait while trying to acquire lock

        timeout=timeout, # lock will be released after timeout if not extended
    )

    # Task for lock extending (only extending, not creating or releasing)
    async def _watchdog():
        nonlocal extend_error
        nonlocal failed_to_extend_lock
        try:
            while True:
                await asyncio.sleep(renew_interval)
                try:
                    # Resets TTL back to timeout seconds
                    # Raises an error if lock expired or was lost
                    extended = await lock.extend(timeout, replace_ttl=True)
                    if not extended:
                        raise RuntimeError(f"Redis lock.extend() returned False for lock '{key}'")
                except Exception as ex:
                    # asyncio.CancelledError does not inherit from Exception, but from BaseException
                    extend_error = ex
                    failed_to_extend_lock = True
                    if owner_task:
                        owner_task.cancel(f"Failed to extend redis lock '{key}'")
                    break
        except asyncio.CancelledError:
            # The watchdog task was canceled from the outside
            pass


    if not await lock.acquire():
        raise TimeoutError(f"Could not acquire lock '{key}' within {acquire_timeout} seconds")

    watchdog_task = asyncio.create_task(_watchdog(), eager_start=True)


    try:
        yield lock
    except asyncio.CancelledError:
        if failed_to_extend_lock:
            raise RedisLockLostError(f"Aborted: lock '{key}' was lost") from extend_error
        raise
    finally:
        watchdog_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await watchdog_task
        if not failed_to_extend_lock:
            with contextlib.suppress(Exception):
                await lock.release()
