import logging
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference

from app.database.schemas import Base
from app.modules.admin.exercises.router import router as admin_exercises_router
from app.modules.admin.user.router import router as admin_user_router
from app.modules.auth.router import router as auth_router
from app.core import config, logger
from app.database.connection import engine
from app.modules.profile.router import router as profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Excerises", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(admin_user_router)
app.include_router(admin_exercises_router)

add_scalar_reference(
    app,
    route="/scalar",
)


@app.get("/")
def hello_world():
    return {"message": "Hello from Excerises!"}


if __name__ == "__main__":
    logger.log.info(
        f"Application running in http://localhost:{config.settings.APP_PORT}"
    )
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.settings.APP_PORT,
        reload=True,
        log_level=logging.ERROR,
    )
