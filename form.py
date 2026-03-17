from fastapi import FastAPI, Form
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="FastAPI Form Demo",
    description="Demonstrates handling HTML form data in FastAPI",
    version="1.0"
)


# 1. Basic Form Parameters
@app.post("/login/")
async def login(
    username: str = Form(..., description="Your username"),
    password: str = Form(..., description="Your password")
):
    return {"username": username, "password": password}



# 2. Optional Form Fields
@app.post("/signup/")
async def signup(
    username: str = Form(...),
    password: str = Form(...),
    email: Optional[str] = Form(None, description="Optional email")
):
    return {"username": username, "password": password, "email": email}



# 3. Using Pydantic Models for Forms
class UserForm(BaseModel):
    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="Password for login")
    email: Optional[str] = Field(None, description="Optional email")

    class Config:
        extra = "forbid"  

@app.post("/user-form/")
async def user_form(
    username: str = Form(...),
    password: str = Form(...),
    email: Optional[str] = Form(None)
):
    user = UserForm(username=username, password=password, email=email)
    return {"user": user}

