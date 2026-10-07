from contextlib import asynccontextmanager
from fastapi import FastAPI

# Импортируем ваш engine базы данных
from db_connection import init_db

from api.user import router as user_router


# Создаем lifespan-функцию, которая выполнится строго при старте приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этот код выполняется ПРИ СТАРТЕ приложения.
    init_db()
    yield



# Create the FastAPI instance
app = FastAPI(lifespan=lifespan)



# Define a GET route at the root URL
@app.get("/")
def read_root():
    return { "Hello": "World" }



# Define a dynamic route with a path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}



app.include_router(user_router)