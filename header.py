from fastapi import FastAPI, Header
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="FastAPI Headers Demo",
    description="Demonstrates handling HTTP headers in FastAPI",
    version="1.0"
)


# 1. Basic Header Parameter
@app.get("/get-header/")
async def get_header(
    user_agent: Optional[str] = Header(None, description="User-Agent header")
):
    return {"user_agent": user_agent}



# 2. Automatic Conversion
@app.get("/convert-header/")
async def convert_header(
    content_length: Optional[int] = Header(None, description="Content-Length header")
):
    return {"content_length": content_length}



# 3. Duplicate Headers
@app.get("/duplicate-header/")
async def duplicate_header(
    x_token: Optional[List[str]] = Header(None, description="Duplicate X-Token headers")
):
    return {"x_token": x_token}



# 4. Using Pydantic Model for Headers
class HeaderModel(BaseModel):
    user_agent: str = Field(..., description="User-Agent header")
    x_token: Optional[str] = Field(None, description="Optional X-Token header")

    class Config:
        extra = "forbid"  
        allow_population_by_field_name = True  

@app.get("/headers-model/")
async def headers_model(
    user_agent: str = Header(...),
    x_token: Optional[str] = Header(None, alias="X-Token")
):
    headers = HeaderModel(user_agent=user_agent, x_token=x_token)
    return {"headers": headers}



# 5. Disable Automatic Underscore Conversion
@app.get("/disable-underscore/")
async def disable_underscore(
    custom_header: Optional[str] = Header(None, convert_underscores=False)
):
    return {"custom_header": custom_header}

