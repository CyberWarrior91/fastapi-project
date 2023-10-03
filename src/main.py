from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from fastapi_users import FastAPIUsers
from src.auth.base_config import auth_backend
from src.auth.models import User
from .operations.router import router as router_operation
from .tasks.router import router as router_tasks
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from src.pages.router import router as router_pages
from src.chat.router import router as router_chat
from .config import REDIS_HOST, REDIS_PORT


app = FastAPI(
    title='Trading App'
)

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET, POST, OPTIONS, DELETE, PATCH, PUT"],
    allow_headers=[
        "Content-Type", 
        "Set-Cookie", 
        "Access-Control-Allow-Headers", 
        "Access-Control-Allow-Origin"
    ],
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


class Paginator:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip


@app.get("/subjects_class")
async def get_subjects_class(pagination_params: Paginator = Depends()):
    return pagination_params


class AuthGuard:
    def __init__(self, name):
        self.name = name

    def __call__(self, request: Request):
        if "super_cookie" not in request.cookies:
            raise HTTPException(status_code=403, detail="Запрещено")
        # проверяем что в куках есть информация о наличии прав пользователя
        return True


auth_guard_payments = AuthGuard("payments")

@app.get("/payments", dependencies=[Depends(auth_guard_payments)])
def get_payments():
    return "my payments:..."


current_user = fastapi_users.current_user()


app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
