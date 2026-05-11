from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_tables
from .api.routes.todos import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)