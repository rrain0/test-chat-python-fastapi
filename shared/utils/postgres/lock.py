import hashlib
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import text


async def postgres_lock(
        postgres: AsyncSession,
        key: str,
):
    await postgres.exec(
        text("SELECT pg_advisory_xact_lock(:key)"),
        params={"key": pg_lock_key_str_to_int(key)},
    )


def pg_lock_key_str_to_int(lock_key_str: str) -> int:
    # Convert lock_key_str into a signed 64-bit integer for pg_advisory_xact_lock(bigint)
    digest = hashlib.sha256(f"single_chat:{lock_key_str}".encode()).digest()
    return int.from_bytes(digest[:8], byteorder="big", signed=True)
