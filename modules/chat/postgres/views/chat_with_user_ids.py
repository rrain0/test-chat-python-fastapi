from uuid import UUID
from typing import List
from sqlmodel import SQLModel, select, func

from modules.chat.postgres.tables.chat_to_user import PgChatToUser


class PgChatWithUserIdsView(SQLModel):
    id: UUID
    user_ids: List[UUID]


# 1. Сначала пишем чистый SQL-запрос сборки данных, который и будет нашим "View".
# Собираем chat_id и массив всех user_id, которые в нем состоят.
chat_with_user_ids_select = (
    select(
        PgChatToUser.chat_id.label("id"),
        # array_agg соберет все UUID пользователей чата в один массив PostgreSQL
        func.array_agg(PgChatToUser.user_id).label("user_ids")
    )
    .group_by(PgChatToUser.chat_id)
)


# Связываем Pydantic-класс с подзапросом через императивный маппинг SQLAlchemy
SQLModel._sa_registry.map_imperatively(
    PgChatWithUserIdsView,
    chat_with_user_ids_select.subquery(),
    primary_key=[chat_with_user_ids_select.subquery().c.id]
)
