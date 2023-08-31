from fastapi import APIRouter

from app.api import chatgtp

api_router = APIRouter()
api_router.include_router(chatgtp.router, tags=["chatgtp"])
