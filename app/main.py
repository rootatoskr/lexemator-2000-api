from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine
from app.models.base import Base
from app.models.cards import WordCard  # noqa


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()


app = FastAPI(
    title='Lexemator 2000 API',
    lifespan=lifespan,
)


@app.get('/health')
async def health_check() -> dict:
    return {'status': 'ok'}
