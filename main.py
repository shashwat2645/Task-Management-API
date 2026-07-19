from fastapi import FastAPI
from src.utils.db import Base, engine
# from src.tasks.models import TaskModel
from src.tasks.routes import task_routes
from src.user.routes import user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", description="API for managing tasks", version="1.0.0")
app.include_router(task_routes)
app.include_router(user_routes)
