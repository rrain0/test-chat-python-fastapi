import contextlib
import anyio

from redis_fastapi import AsyncRedisDep


class RedisLockLostError(Exception):
    """Raised when the background watchdog fails to extend the Redis lock."""
    pass



@contextlib.asynccontextmanager
async def redis_watchdog_lock(
    redis: AsyncRedisDep,
    key: str,
    acquire_timeout: float = 11.0,
    renew_interval: float = 1.0,
    timeout: float = 3.0,
):
    key = f'lock:{key}'
    lock_extend_is_failed = False
    lock_extend_error: Exception | None = None

    lock = redis.lock(
        name=key,

        sleep=0.2, # interval to check lock while trying to acquire lock
        blocking=True, # wait for lock to be available or time runs out while trying to acquire lock
        blocking_timeout=acquire_timeout, # maximum amount of time to wait while trying to acquire lock

        timeout=timeout, # lock will be released after timeout if not extended
    )

    # Task for lock extending (only extending, not creating or releasing)
    async def _watchdog(scope: anyio.CancelScope):
        nonlocal lock_extend_error
        nonlocal lock_extend_is_failed
        while True:
            await anyio.sleep(renew_interval)
            try:
                # Resets TTL back to timeout seconds
                # Raises an error if lock expired or was lost
                extended = await lock.extend(timeout, replace_ttl=True)
                if not extended:
                    raise RuntimeError(f"Redis lock.extend() returned False for lock '{key}'")
            except Exception as ex:
                # asyncio.CancelledError does not inherit from Exception, but from BaseException
                lock_extend_is_failed = True
                lock_extend_error = ex
                scope.cancel()
                break



    if not await lock.acquire():
        raise TimeoutError(f"Could not acquire lock '{key}' within {acquire_timeout} seconds")


    try:
        with anyio.CancelScope() as scope:
            async with anyio.create_task_group() as tg:
                tg.start_soon(_watchdog, scope)
                try:
                    yield lock
                finally:
                    # Stop the watchdog when the yielded block finishes normally or with an error
                    tg.cancel_scope.cancel()

        if lock_extend_is_failed:
            raise RedisLockLostError(f"Aborted: redis lock '{key}' was lost") from lock_extend_error
    finally:
        if not lock_extend_is_failed:
            # Shield release so an outer cancellation still cleans up the Redis lock
            with anyio.CancelScope(shield=True):
                with contextlib.suppress(Exception):
                    await lock.release()
