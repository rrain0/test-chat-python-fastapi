from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api_model.api_error import ApiError
from db_connection.db_connection import init_db

from api_routes.user_signup import user_signup_router
from api_routes.user_login import user_login_router
from api_routes.user_current import user_current_router
from api_routes.tg_user_post_message import tg_user_post_message_router


# Создаем lifespan-функцию, которая выполнится строго при старте приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этот код выполняется ПРИ СТАРТЕ приложения.
    init_db()
    yield



# Create the FastAPI instance
app = FastAPI(lifespan=lifespan)

app.include_router(user_signup_router)
app.include_router(user_login_router)
app.include_router(user_current_router)
app.include_router(tg_user_post_message_router)



# Перехватываем стандартную ошибку валидации запроса
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ApiError(
                error_code="DATA_FORMAT_ERROR",
                msg="Неправильный формат входных данных",
                detail=errors,
            )
        )
    )


# Define a GET route at the root URL
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Define a dynamic route with a path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
