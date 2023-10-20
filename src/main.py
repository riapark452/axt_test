import logging

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.app.router import router as app_router
from src.auth.router import router as auth_router

logger = logging.getLogger(__name__)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=app_router, prefix="/users", tags=["Users"])
app.include_router(router=auth_router, prefix="/auth", tags=["Auth"])


@app.get("/", tags=["root"])
async def read_root() -> dict:
    logger.info(f"request / endpoint!")
    return {"message": "Welcome to API!"}
