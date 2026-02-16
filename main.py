from fastapi import FastAPI
from database import engine, Base
from routers import user_routes, project_routes, task_routes

app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)

@app.get("/")
def message():
    return {"message": "Mini Project Management System"}