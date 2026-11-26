from uuid import UUID, uuid7

from sqlmodel import select

from modules.chat.postgres.key.create_user_chat import pg_get_create_user_chat_key
from modules.chat.postgres.tables.chat import PgChat
from modules.chat.postgres.tables.chat_to_user import PgChatToUser
from modules.chat.postgres.views.chat_with_user_ids import PgChatWithUserIdsView
from shared.utils.postgres.async_postgres import AsyncPostgres
from shared.utils.postgres.lock import postgres_lock


async def pg_upsert_chat_of_single_user(
        user_id: UUID,
        postgres: AsyncPostgres,
):
    async def get_chat_view():
        return (await postgres.exec(
            select(PgChatWithUserIdsView)
            .where(PgChatWithUserIdsView.user_ids == [user_id])
        )).first()

    # 1. Fast-path check without taking a lock
    # Find an existing single-user chat
    chat_view = await get_chat_view()

    if chat_view:
        return chat_view

    # 2. Acquire a transaction-level lock specific to this user_id & chat create action
    await postgres_lock(
        pg_get_create_user_chat_key(user_id),
        postgres,
    )

    # 3. Double-check AFTER acquiring the lock!
    # Another request might have finished creating the chat while we were waiting.
    chat_view = await get_chat_view()

    if chat_view:
        return chat_view


    # 4. Safely create a new chat under lock

    new_chat = PgChat(id=uuid7())
    postgres.add(new_chat)
    await postgres.flush()
    await postgres.refresh(new_chat)

    new_chat_to_user = PgChatToUser(chat_id=new_chat.id, user_id=user_id)
    postgres.add(new_chat_to_user)
    await postgres.flush()

    new_chat_view = (await postgres.exec(
        select(PgChatWithUserIdsView)
        .where(PgChatWithUserIdsView.id == new_chat.id)
    )).one()

    return new_chat_view


# TODO
#  and if frontend doubles random chat creation request? Chats can be identical and id is generated on backend
#    Use a client-generated Idempotency-Key header with Redis or client-generated chat_id UUID.
