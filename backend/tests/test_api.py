from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
import pytest

client = TestClient(app)

def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_full_flow():
    # register user
    r = client.post('/auth/register', json={'username':'tester','password':'strongpassword'})
    assert r.status_code == 201
    # token
    r2 = client.post('/auth/token', data={'username':'tester','password':'strongpassword'})
    assert r2.status_code == 200
    token = r2.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    # create employee
    r = client.post('/employees/', json={'first_name':'Alice','last_name':'Doe','email':'alice@example.com'}, headers=headers)
    assert r.status_code == 201
    emp = r.json()
    emp_id = emp['id']
    # create task assigned to employee
    r = client.post('/tasks/', json={'title':'task-1','description':'new-task','employee_id': emp_id}, headers=headers)
    assert r.status_code == 201
    task = r.json()
    task_id = task['id']
    # reassign task to null (unassign)
    r = client.patch(f'/tasks/{task_id}/assign', json={'employee_id': None}, headers=headers)
    assert r.status_code == 200
    # assign to non-existing - should 404
    r = client.patch(f'/tasks/{task_id}/assign', json={'employee_id': 9999}, headers=headers)
    assert r.status_code == 404
    # delete task
    r = client.delete(f'/tasks/{task_id}', headers=headers)
    assert r.status_code == 204
    # delete employee
    r = client.delete(f'/employees/{emp_id}', headers=headers)
    assert r.status_code == 204
