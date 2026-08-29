from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================
# Reusable Schema Mixins
# ==========================================
class UserAuditSchemaMixin(BaseModel):
    """Mixin for models requiring created_by_id and updated_by_id on creation."""

    created_by_id: int = Field(
        gt=0, description="ID of the authenticated user creating this record"
    )
    updated_by_id: int = Field(
        gt=0, description="ID of the authenticated user performing this operation"
    )


class UserAuditUpdateSchemaMixin(BaseModel):
    """Mixin for models requiring optional updated_by_id on update payloads."""

    updated_by_id: int | None = Field(
        default=None,
        gt=0,
        description="ID of the authenticated user updating this record",
    )


class ActiveFieldUpdateSchemaMixin(BaseModel):
    """Mixin for models requiring optional active on update payloads."""

    active: bool | None = Field(
        default=None, description="Optional active status toggle"
    )


class TimestampSchemaMixin(BaseModel):
    """Mixin for models returning timestamp & active status fields to the client."""

    active: bool = Field(
        default=True,
        description="Soft-delete status flag (True for active, False for disabled)",
    )
    created_at: datetime = Field(
        description="Timestamp (UTC) when this record was originally created"
    )
    updated_at: datetime = Field(
        description="Timestamp (UTC) when this record was last modified"
    )


class IDSchemaMixin(BaseModel):
    """Mixin providing database primary key ID & ORM attributes support."""

    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------


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
class UserUpdate(ActiveFieldUpdateSchemaMixin):
    email: EmailStr | None = Field(default=None, max_length=128)


# Properties shared by models stored in DB
class UserInDBBase(UserPublicBase, IDSchemaMixin):
    pass


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
class TaskUpdate(ActiveFieldUpdateSchemaMixin):
    name: str | None = Field(default=None, min_length=1, max_length=250)
    completed: bool | None = Field(default=None)


# Properties shared by models stored in DB
class TaskInDBBase(TaskBase, IDSchemaMixin):
    owner_id: int
    owner: UserInDBBase


#############################


# ---------------------------------------------


# ==========================================
# Properties to return to client
# ==========================================
class User(UserInDBBase, TimestampSchemaMixin):
    pass


class Task(TaskInDBBase, TimestampSchemaMixin):
    pass


# ---------------------------------------------


# ==========================================
# Properties stored in DB
# ==========================================
class UserInDB(UserInDBBase, TimestampSchemaMixin):
    pass


class TaskInDB(TaskInDBBase, TimestampSchemaMixin):
    pass
