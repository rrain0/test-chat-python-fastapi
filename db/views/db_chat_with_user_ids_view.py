import uuid
from typing import List
from sqlmodel import SQLModel, select, func

from db.tables.db_chat_to_user import DbChatToUser

# 1. Сначала пишем чистый SQL-запрос сборки данных, который и будет нашим "View".
# Собираем chat_id и массив всех user_id, которые в нем состоят.
chat_with_user_ids_select = (
    select(
        DbChatToUser.chat_id.label("id"),
        # array_agg соберет все UUID пользователей чата в один массив PostgreSQL
        func.array_agg(DbChatToUser.user_id).label("user_ids")
    )
    .group_by(DbChatToUser.chat_id)
)


class DbChatWithUserIdsView(SQLModel):
    id: uuid.UUID
    user_ids: List[uuid.UUID]



# Связываем Pydantic-класс с подзапросом через императивный маппинг SQLAlchemy
SQLModel._sa_registry.map_imperatively(
    DbChatWithUserIdsView,
    chat_with_user_ids_select.subquery(),
    primary_key=[chat_with_user_ids_select.subquery().c.id]
)
