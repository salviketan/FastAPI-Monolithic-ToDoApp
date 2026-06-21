from app.core.base_crud import CRUDBase
from app.models import Tasks, Users
from app.schemas import TaskCreate, TaskUpdate, UserCreate, UserUpdate


class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):
    pass


class CRUDTask(CRUDBase[Tasks, TaskCreate, TaskUpdate]):
    pass


user = CRUDUser(Users)
task = CRUDTask(Tasks)
