from contextlib import asynccontextmanager
from typing import AsyncGenerator

from starlette.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.home.router import router as home_router
from src.config import get_settings
from src.db import database
import uvicorn


# @asynccontextmanager
# async def lifespan(_application: FastAPI) -> AsyncGenerator:
#     # Startup
#     await database.create_db_conn_pool()

#     yield

#     # Shutdown
#     await database.close_db_conn_pool()

# app = FastAPI(lifespan=lifespan)


app = FastAPI()

settings = get_settings()
print(settings.CORS_ALLOW_ORIGINS)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
    allow_credentials=True,
)

# Initialize the database
@app.on_event("startup")
async def startup():
    await database.create_db_conn_pool()

@app.on_event("shutdown")
async def shutdown():
    await database.close_db_conn_pool()

# Register routes here
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(home_router)



if __name__ == "__main__":
    uvicorn(app, host="0.0.0.0", port=5000, reload=True, app_dir="/home/tim/CS/coding/online_conference/online_conference_backend/")