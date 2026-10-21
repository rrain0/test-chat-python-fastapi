from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend_api_model.back_api_error import BackApiError
from api.routes.tg_user_login_post import tg_user_login_router
from db.connection.db_connection import init_db

from api.routes.user_signup_post import user_signup_router
from api.routes.user_login_post import user_login_router
from api.routes.user_current_get import user_current_router
from api.routes.tg_user_msg_post import tg_user_msg_router


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
app.include_router(tg_user_login_router)
app.include_router(user_current_router)
app.include_router(tg_user_msg_router)



# Перехватываем стандартную ошибку валидации запроса
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            BackApiError(
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
