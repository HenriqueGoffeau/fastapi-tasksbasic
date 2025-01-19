from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False

tasks: List[Task] = []

@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    if any(e.id == task.id for e in tasks):
        raise HTTPException(status_code=400, detail="Task já existente")
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}/", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task não encontrada.")

@app.put("/tasks/{task_id}/", response_model=Task)
async def updtate_task(task_id: int, updated_task: Task):
    for index, task in enumarate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
        raise HTTPException(status_code=404, detail="Task não encontrada.")