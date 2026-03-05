from fastapi import FastAPI, Cookie
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="FastAPI Cookies Demo",
    description="Demonstrates handling cookies in FastAPI",
    version="1.0"
)


# 1. Basic Cookie Parameter
@app.get("/get-cookie/")
async def get_cookie(
    session_id: Optional[str] = Cookie(None, description="Session ID cookie")
):
    return {"session_id": session_id}


# 2. Multiple Cookie Parameters
@app.get("/get-multiple-cookies/")
async def get_multiple_cookies(
    session_id: Optional[str] = Cookie(None),
    user_token: Optional[str] = Cookie(None)
):
    """
    Endpoint with multiple cookies.
    """
    return {"session_id": session_id, "user_token": user_token}



# 3. Using Pydantic Model for Cookies
class CookieModel(BaseModel):
    session_id: str = Field(..., description="Session ID cookie")
    user_token: str = Field(..., description="User token cookie")

    class Config:
        extra = "forbid" 


@app.get("/cookies-model/")
async def cookies_model(
    session_id: str = Cookie(...),
    user_token: str = Cookie(...)
):
    cookies = CookieModel(session_id=session_id, user_token=user_token)
    return {"cookies": cookies}

