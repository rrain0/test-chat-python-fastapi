import asyncio
import contextlib
from redis_fastapi import AsyncRedisDep



class LockLostError(asyncio.CancelledError):
    """Raised when the background watchdog fails to extend the Redis lock."""
    pass


@contextlib.asynccontextmanager
async def redis_watchdog_lock(
    redis: AsyncRedisDep,
    key: str,
    timeout: float = 2.0,
    renew_interval: float = 1.0,
    blocking_timeout: float = 5.0,
):
    owner_task = asyncio.current_task()
    lost_event = asyncio.Event()
    lock = redis.lock(key, timeout=timeout, blocking_timeout=blocking_timeout)

    if not await lock.acquire():
        raise TimeoutError(f'Could not acquire lock "{key}"')

    async def _watchdog():
        try:
            while True:
                await asyncio.sleep(renew_interval)
                try:
                    # Resets TTL back to 2.0s; raises an error if lock expired or was lost
                    extended = await lock.extend(timeout, replace_ttl=True)
                    if not extended:
                        raise RuntimeError('Redis lock extension was failed')
                except Exception:
                    lost_event.set()
                    if owner_task and not owner_task.done():
                        owner_task.cancel('Redis lock expired or lost')
                    break
        except asyncio.CancelledError:
            pass

    watchdog_task = asyncio.create_task(_watchdog())
    try:
        yield lock
    except asyncio.CancelledError as ex:
        if lost_event.is_set():
            raise LockLostError(f'Aborted: lock "{key}" was lost') from ex
        raise
    finally:
        watchdog_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await watchdog_task
        if not lost_event.is_set():
            with contextlib.suppress(Exception):
                await lock.release()
