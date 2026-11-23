import asyncio
import contextlib

from redis_fastapi import AsyncRedisDep



class RedisLockLostError(asyncio.CancelledError):
    """Raised when the background watchdog fails to extend the Redis lock."""
    pass



@contextlib.asynccontextmanager
async def redis_watchdog_lock(
    redis: AsyncRedisDep,
    key: str,
    timeout: float = 2.0,
    renew_interval: float = 1.0,
    acquire_timeout: float = 6.0,
):
    owner_task = asyncio.current_task()
    lock_lost = asyncio.Event()
    lock = redis.lock(
        name=key,

        sleep=0.2, # interval to check lock while trying to acquire lock
        blocking=True, # wait for lock to be available or time runs out while trying to acquire lock
        blocking_timeout=acquire_timeout, # maximum amount of time to wait while trying to acquire lock

        timeout=timeout, # lock will be released after timeout if not extended
    )

    if not await lock.acquire():
        raise TimeoutError(f"Could not acquire lock '{key}' within {acquire_timeout} seconds")

    async def _watchdog():
        try:
            while True:
                await asyncio.sleep(renew_interval)
                try:
                    # Resets TTL back to timeout seconds
                    # Raises an error if lock expired or was lost
                    extended = await lock.extend(timeout, replace_ttl=True)
                    if not extended:
                        raise RuntimeError("Failed to extend redis lock")
                except Exception:
                    lock_lost.set()
                    if owner_task and not owner_task.done():
                        owner_task.cancel("Redis lock expired or lost")
                    break
        except asyncio.CancelledError:
            pass

    watchdog_task = asyncio.create_task(_watchdog())
    try:
        yield lock
    except asyncio.CancelledError as ex:
        if lock_lost.is_set():
            raise RedisLockLostError(f"Aborted: lock '{key}' was lost") from ex
        raise
    finally:
        watchdog_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await watchdog_task
        if not lock_lost.is_set():
            with contextlib.suppress(Exception):
                await lock.release()
