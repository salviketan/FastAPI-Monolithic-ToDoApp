from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


##### Task Table Schema #####
# Shared properties
class TaskBase(BaseModel):
    name: str = Field(min_length=1, max_length=250)
    completed: bool = Field(default=False)


# Properties to receive on Task creation
class TaskCreate(TaskBase):
    pass


# Properties to receive on Task update
class TaskUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=250)
    completed: bool | None = Field(default=None)
    active: bool | None = Field(default=None)


# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# ---------------------------------------------


# Properties to return to client
class Task(TaskInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------


# Properties stored in DB
class TaskInDB(TaskInDBBase):
    pass
