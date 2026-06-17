from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.cards import router as cards_router
from app.core.database import engine
from app.models.base import Base


# Ініціалізація БД при старті, звільнення з'єднань при зупинці
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()


app = FastAPI(
    title='Lexemator 2000 API',
    lifespan=lifespan,
)
app.include_router(cards_router)


@app.get('/health')
async def health_check() -> dict[str, str]:
    return {'status': 'ok'}
