from fastapi import HTTPException

from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.user.models import UserModel

def create_task(body: TaskSchema, db:Session, user: UserModel):
    data = body.model_dump()
    new_task = TaskModel(title=data['title'], description=data['description'], is_completed=data['is_completed'], user_id = user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_tasks(db:Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks


def get_one_task(task_id:int, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not task:
        raise HTTPException(404, detail="No task not found")
    return task


def update_task(task_id:int, body:TaskSchema, db:Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not task:
        raise HTTPException(404, detail = "No such task exists")
    
    update_data = body.model_dump()

    for field, value in update_data.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(task_id:int, db:Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(404, detail = "No such task exists")

    if task.user_id != user.id:
        raise HTTPException(401, detail="You don't have permission to delete this task")
    
    db.delete(task)
    db.commit()
    return None