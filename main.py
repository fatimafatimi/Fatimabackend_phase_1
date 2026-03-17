from fastapi import FastAPI
from database import engine, Base
from routers.user_routes import user_router
from routers.project_routes import project_router
from routers.task_routes import task_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def welcome():
    return {"message": "Mini Project Management System"}
