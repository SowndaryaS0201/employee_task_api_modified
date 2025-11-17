from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=schemas.EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(employee_in: schemas.EmployeeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = crud.get_employee_by_email(db, employee_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_employee(db, employee_in)

@router.get("/", response_model=List[schemas.EmployeeOut])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    rows = crud.list_employees(db, skip, limit)
    # rows are tuples (Employee, task_count)
    result = []
    for emp, count in rows:
        obj = emp.__dict__.copy()
        obj.pop('_sa_instance_state', None)
        obj['task_count'] = count
        obj['tasks'] = [ {k:v for k,v in t.__dict__.items() if k!='_sa_instance_state'} for t in emp.tasks ]
        result.append(obj)
    return result

@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    tasks = crud.list_tasks_for_employee(db, employee_id)
    emp.task_count = len(tasks)
    return emp

@router.put("/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(employee_id: int, updates: schemas.EmployeeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return crud.update_employee(db, emp, updates)

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    crud.delete_employee(db, emp)
    return

@router.get("/{employee_id}/tasks", response_model=List[schemas.TaskOut])
def list_employee_tasks(employee_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return crud.list_tasks_for_employee(db, employee_id, skip, limit)

@router.post("/{employee_id}/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_for_employee(employee_id: int, task_in: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return crud.create_task(db, task_in, employee_id)
