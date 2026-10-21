import uuid

from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select

from db.tables.db_chat import DbChat
from db.tables.db_chat_to_user import DbChatToUser
from db.tables.db_tg_user import DbTgUser
from db.views.db_chat_with_user_ids_view import DbChatWithUserIdsView



def upsert_chat_of_single_user(session: Session, user_id: uuid.UUID):
    # 1. Ищем существующий одиночный чат пользователя.
    chat_view = session.exec(
        select(DbChatWithUserIdsView)
        .where(DbChatWithUserIdsView.user_ids == [user_id])
    ).first()

    if chat_view: return chat_view

    # Открываем явный блок транзакции/сохранения
    with session.begin_nested():

        # 2. Если чата нет — создаем сам чат

        new_chat = DbChat()  # UUID сгенерируется на стороне Python автоматически
        session.add(new_chat)
        session.flush()
        session.refresh(new_chat)

        new_chat_to_user = DbChatToUser(chat_id=new_chat.id, user_id=user_id)
        session.add(new_chat_to_user)
        session.flush()


        new_chat_view = session.exec(
            select(DbChatWithUserIdsView)
            .where(DbChatWithUserIdsView.id == new_chat.id)
        ).one()

        return new_chat_view




def db_get_tg_user_by_id(session: Session, id: int) -> DbTgUser | None:
    return session.exec(select(DbTgUser).where(DbTgUser.id == id)).first()



def db_upsert_tg_user(session: Session, db_tg_user: DbTgUser) -> None:
    statement = insert(DbTgUser).values(
        id=db_tg_user.id,
        user_id=db_tg_user.user_id,
        username=db_tg_user.username,
        first_name=db_tg_user.first_name,
        last_name=db_tg_user.last_name,
    )

    # If the ID already exists, update these fields
    statement = statement.on_conflict_do_update(
        index_elements=["id"],
        set_={
            "user_id": statement.excluded.user_id,
            "username": statement.excluded.username,
            "first_name": statement.excluded.first_name,
            "last_name": statement.excluded.last_name,
        }
    )

    session.exec(statement)
    session.commit()
