from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.core.redis import close_redis
from app.routes import players_router, rankings_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.dev_mode:
        await init_db()
    yield
    if not settings.dev_mode:
        await close_redis()


app = FastAPI(
    title="PUBG Plus API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players_router)
app.include_router(rankings_router)


@app.get("/health")
async def health():
    return {"status": "ok", "mode": "dev" if settings.dev_mode else "prod"}
