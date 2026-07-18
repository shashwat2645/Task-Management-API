from fastapi import HTTPException

from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel

def create_task(body: TaskSchema, db:Session):
    data = body.model_dump()
    new_task = TaskModel(title=data['title'], description=data['description'], is_completed=data['is_completed'])

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    return tasks


def get_one_task(task_id:id, db: Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(404, detail="No task not found")
    return task


def update_task(task_id:int, body:TaskSchema, db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(404, detail = "No such task exists")
    
    body = body.model_dump()

    for field, value in body.items():
        setattr(task, field, value)

    # task.title = body.title
    # task.description = body.description
    # task.is_completed = body.is_completed

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(task_id:int, db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(404, detail = "No such task exists")
    
    db.delete(task)
    db.commit()
    return None