from sqlalchemy.orm import Session
from . import models, schemas, security
from typing import List, Optional
from sqlalchemy import func

# User operations
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

# Employee CRUD
def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def list_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    # include task_count via join
    rows = db.query(models.Employee, func.count(models.Task.id).label('task_count')).outerjoin(models.Task).group_by(models.Employee.id).offset(skip).limit(limit).all()
    # return as list of tuples (Employee, task_count)
    return rows

def create_employee(db: Session, emp_in: schemas.EmployeeCreate) -> models.Employee:
    emp = models.Employee(**emp_in.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

def update_employee(db: Session, emp: models.Employee, updates: schemas.EmployeeUpdate):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(emp, field, value)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

def delete_employee(db: Session, emp: models.Employee):
    db.delete(emp)
    db.commit()

# Task CRUD
def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def list_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()

def list_tasks_for_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.employee_id == employee_id).offset(skip).limit(limit).all()

def create_task(db: Session, task_in: schemas.TaskCreate, employee_id: int = None) -> models.Task:
    payload = task_in.dict()
    if employee_id:
        payload["employee_id"] = employee_id
    # allow employee_id provided in task_in too
    if payload.get('employee_id') is None and task_in.employee_id:
        payload['employee_id'] = task_in.employee_id
    task = models.Task(**payload)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task: models.Task, updates: schemas.TaskUpdate):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def assign_task(db: Session, task: models.Task, employee_id: Optional[int]):
    task.employee_id = employee_id
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()
