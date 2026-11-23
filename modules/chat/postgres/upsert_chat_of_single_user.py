from uuid import UUID, uuid7

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.chat.postgres.chat import DbChat
from modules.chat.postgres.chat_to_user import DbChatToUser
from modules.chat.postgres.chat_with_user_ids_view import DbChatWithUserIdsView


async def upsert_chat_of_single_user(postgres: AsyncSession, user_id: UUID):
    # 1. Find an existing single-user chat
    chat_view = (await postgres.exec(
        select(DbChatWithUserIdsView)
        .where(DbChatWithUserIdsView.user_ids == [user_id])
    )).first()

    if chat_view: return chat_view

    # Открываем явный блок транзакции/сохранения
    async with postgres.begin_nested():

        # 2. Если чата нет — создаем сам чат

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
