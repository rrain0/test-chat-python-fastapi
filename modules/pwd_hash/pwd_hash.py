import asyncio
import bcrypt
import base64
import hashlib



def _prehash(pwd: str) -> bytes:
    # password string  -> 32 raw bytes  -> 44 ASCII Base64 bytes
    # (no null bytes, always < 72 bytes for bcrypt)
    digest = hashlib.sha256(pwd.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_pwd(pwd: str) -> str:
    # Случайная соль для каждого пароля
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(_prehash(pwd), salt).decode("utf-8")

def verify_pwd(pwd: str, pwd_hash: str) -> bool:
    return bcrypt.checkpw(_prehash(pwd), pwd_hash.encode("utf-8"))


async def hash_pwd_athread(pwd: str) -> str:
    return await asyncio.to_thread(lambda: hash_pwd(pwd))

async def verify_pwd_athread(pwd: str, pwd_hash: str) -> bool:
    return await asyncio.to_thread(lambda: verify_pwd(pwd, pwd_hash))
