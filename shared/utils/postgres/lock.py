import hashlib
from sqlalchemy import text

from shared.utils.postgres.async_postgres import AsyncPostgres



# Advisory Lock is bound to transaction
# and automatically releases when COMMIT, ROLLBACK or CONNECTION DROP
async def postgres_lock(
        key: str,
        postgres: AsyncPostgres,
):
    await postgres.exec(
        text("SELECT pg_advisory_xact_lock(:key)"),
        params={"key": pg_lock_key_str_to_int(key)},
    )


def pg_lock_key_str_to_int(lock_key_str: str) -> int:
    # Convert lock_key_str into a signed 64-bit integer for pg_advisory_xact_lock(bigint)
    digest = hashlib.sha256(lock_key_str.encode()).digest()
    return int.from_bytes(digest[:8], byteorder="big", signed=True)
