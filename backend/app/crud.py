from app.core.base_crud import CRUDBase
from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    pass


user = CRUDUser(User)
task = CRUDTask(Task)
