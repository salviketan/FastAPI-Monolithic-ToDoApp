from api.api_v1.endpoints import tasks
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
