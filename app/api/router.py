from fastapi import APIRouter
from app.api.routes import items, categories, auth

api_router = APIRouter()
api_router.include_router(items.router)
api_router.include_router(categories.router)
api_router.include_router(auth.router)