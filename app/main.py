from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from .models import Tasks
from .schemas import TaskCreate, TaskBase
from fastapi import APIRouter
from .database import get_db

app = APIRouter()
@app.get("/tasks/", response_model=List[TaskCreate])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Tasks).all()

@app.post("/tasks/", response_model=List[TaskCreate])
def create_task(task: TaskBase, db: Session = Depends(get_db)):
    new_task = Tasks(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return [new_task]

@app.get("/tasks/{task_id}/", response_model=TaskCreate)
def get_one_task(task_id:int, db:Session = Depends(get_db)):
    idv_task = db.query(Tasks).filter(Tasks.id == task_id).first()
    
    if idv_task is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A task específica não existe")
    return idv_task

@app.put("/tasks/{task_id}/", response_model=TaskCreate)
def update_task(task_data:TaskBase, task_id:int, db:Session = Depends(get_db)):
    task_query = db.query(Tasks).filter(Tasks.id == task_id)
    
    if task_query.first() is None:
        raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail=f"A task específica não existe")
    task_query.update(task_data.dict(), synchronize_session=False)
    db.commit()
    
    return task_query.first()

@app.delete("/tasks/{task_id}/")
def delete_task(task_id:int, db:Session = Depends(get_db)):
    deleted_task = db.query(Tasks).filter(Tasks.id == task_id)
    
    if deleted_task.first() is None:
        raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail=f"A task específica não existe")
    deleted_task.delete(synchronize_session=False)
    db.commit()