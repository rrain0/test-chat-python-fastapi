from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.chat.db_tables.chat import DbChat
from modules.chat.db_tables.chat_to_user import DbChatToUser
from modules.chat.db_views.chat_with_user_ids_view import DbChatWithUserIdsView


async def upsert_chat_of_single_user(postgres: AsyncSession, user_id: UUID):
    # 1. Ищем существующий одиночный чат пользователя.
    chat_view = (await postgres.exec(
        select(DbChatWithUserIdsView)
        .where(DbChatWithUserIdsView.user_ids == [user_id])
    )).first()

    if chat_view: return chat_view

    # Открываем явный блок транзакции/сохранения
    async with postgres.begin_nested():

        # 2. Если чата нет — создаем сам чат

        new_chat = DbChat()  # UUID сгенерируется на стороне Python автоматически
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
