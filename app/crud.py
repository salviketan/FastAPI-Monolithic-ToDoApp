from core.base_crud import CRUDBase
from models import Task
from schemas import TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    pass


task = CRUDTask(Task)
