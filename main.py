from fastapi import FastAPI
from routers import tasks
from config import engine, Base
from models import task

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def welcome():
    return {"message": "Welcome"}
