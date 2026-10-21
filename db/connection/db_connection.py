from sqlmodel import create_engine, Session, SQLModel

# Replace with your actual PostgreSQL credentials
# Format: postgresql://user:password@localhost:port/database_name
DATABASE_URL = "postgresql://backend_db_user:backend_db_user_pwd@localhost:5432/test_chat_python_fastapi_db"

# Import all physical tables to create them in specified order
from db.tables.db_user import DbUser
from db.tables.db_tg_user import DbTgUser
from db.tables.db_chat import DbChat
from db.tables.db_chat_to_user import DbChatToUser
from db.tables.db_msg import DbMsg

# Create the SQLAlchemy/SQLModel engine
engine = create_engine(DATABASE_URL, echo=True)

# Функция, которую мы вызовем в lifespan
def init_db():
    # Печатает в консоль список таблиц, которые SQLModel видит в памяти
    print("Зарегистрированные таблицы:", SQLModel.metadata.tables.keys())
    # Проверяет базу данных и создает таблицы, если их еще нет.
    SQLModel.metadata.create_all(engine)

# Context manager/Dependency to handle session closing automatically
def get_session():
    with Session(engine) as session:
        yield session