from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


##### Task Table Schema #####
# Shared properties
class UserPublicBase(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=16)
    last_name: str | None = Field(default=None, min_length=1, max_length=16)
    username: str | None = Field(default=None, min_length=4, max_length=32)


class UserPrivateBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=16)
    last_name: str = Field(min_length=1, max_length=16)
    email: EmailStr = Field(max_length=128)


# Properties to receive on User creation
class UserCreate(UserPrivateBase):
    password: str = Field(min_length=8)


# Properties to receive on User update
class UserUpdate(UserPublicBase):
    email: EmailStr | None = Field(default=None, max_length=128)
    active: bool | None = Field(default=None)


# Properties shared by models stored in DB
class UserInDBBase(UserPublicBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


#############################


##### Task Table Schema #####
# Shared properties
class TaskBase(BaseModel):
    name: str = Field(min_length=1, max_length=250)
    completed: bool = Field(default=False)
    owner_id: int


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
    # owner_id: int
    owner: UserInDBBase


#############################


# ---------------------------------------------


# Properties to return to client
class User(UserInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


# Properties to return to client
class Task(TaskInDBBase):
    active: bool
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------


# Properties stored in DB
class UserInDB(UserInDBBase):
    pass


# Properties stored in DB
class TaskInDB(TaskInDBBase):
    pass
