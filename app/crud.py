from models import Task
from schemas import TaskCreate, TaskUpdate

from app.core.base_crud import CRUDBase


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    pass


task = CRUDTask(Task)
