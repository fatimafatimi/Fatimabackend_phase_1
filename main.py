from fastapi import FastAPI
from database import engine, Base
from routers import user_routes, project_routes, task_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(project_routes.router, prefix="/projects", tags=["Projects"])
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def welcome():
    return {"message": "Mini Project Management System"}
