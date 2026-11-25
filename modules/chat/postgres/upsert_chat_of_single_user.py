from uuid import UUID, uuid7

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.chat.postgres.get_lock_key_create_user_chat import pg_get_lock_key_create_user_chat
from modules.chat.postgres.chat import DbChat
from modules.chat.postgres.chat_to_user import DbChatToUser
from modules.chat.postgres.chat_with_user_ids_view import DbChatWithUserIdsView
from shared.utils.postgres.lock import postgres_lock


async def pg_upsert_chat_of_single_user(
        user_id: UUID,
        postgres: AsyncSession,
):
    async def get_chat_view():
        return (await postgres.exec(
            select(DbChatWithUserIdsView)
            .where(DbChatWithUserIdsView.user_ids == [user_id])
        )).first()

    # 1. Fast-path check without taking a lock
    # Find an existing single-user chat
    chat_view = await get_chat_view()

    if chat_view:
        return chat_view

    # 2. Acquire a transaction-level lock specific to this user_id & chat create action
    await postgres_lock(
        postgres,
        pg_get_lock_key_create_user_chat(user_id),
    )

    # 3. Double-check AFTER acquiring the lock!
    # Another request might have finished creating the chat while we were waiting.
    chat_view = await get_chat_view()

    if chat_view:
        return chat_view


    # 4. Safely create a new chat under lock

    new_chat = DbChat(id=uuid7())
    postgres.add(new_chat)
    await postgres.flush()
    await postgres.refresh(new_chat)

    new_chat_to_user = DbChatToUser(chat_id=new_chat.id, user_id=user_id)
    postgres.add(new_chat_to_user)
    await postgres.flush()

    new_chat_view = (await postgres.exec(
        select(DbChatWithUserIdsView)
        .where(DbChatWithUserIdsView.id == new_chat.id)
    )).one()

    return new_chat_view
