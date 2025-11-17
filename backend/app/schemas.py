# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
import datetime

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=50) # type: ignore
    password: constr(min_length=6) # type: ignore

class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool
    class Config:
        orm_mode = True

# Tasks
class TaskBase(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=200) # type: ignore
    description: Optional[str] = None
    status: Optional[str] = "todo"
    priority: Optional[int] = 3
    due_date: Optional[str] = None

class TaskCreate(TaskBase):
    employee_id: Optional[int] = None

class TaskAssign(BaseModel):
    employee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1, max_length=200)] # type: ignore
    description: Optional[str]
    status: Optional[str]
    priority: Optional[int]
    due_date: Optional[str]

class TaskOut(TaskBase):
    id: int
    employee_id: Optional[int]
    created_at: Optional[datetime.datetime]
    class Config:
        orm_mode = True

# Employees
class EmployeeBase(BaseModel):
    first_name: constr(min_length=1) # type: ignore
    last_name: constr(min_length=1) # type: ignore
    email: EmailStr
    position: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[constr(min_length=1)] # type: ignore
    last_name: Optional[constr(min_length=1)] # type: ignore
    email: Optional[EmailStr]
    position: Optional[str]
    department: Optional[str]
    is_active: Optional[bool]

class EmployeeOut(EmployeeBase):
    id: int
    created_at: Optional[datetime.datetime]
    task_count: int = 0
    tasks: List[TaskOut] = []
    class Config:
        orm_mode = True
