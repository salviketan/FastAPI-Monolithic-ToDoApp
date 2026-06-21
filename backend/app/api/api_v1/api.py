from fastapi import APIRouter

from app.api.api_v1.endpoints import tasks, users

api_router = APIRouter()

api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
