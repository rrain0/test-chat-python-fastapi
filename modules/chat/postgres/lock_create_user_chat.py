from sqlalchemy.ext.asyncio.session import AsyncSession


async def lock_create_user_chat(postgres: AsyncSession):
