from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="FastAPI Request Body Demo",
    description="Demonstrates using request bodies in FastAPI",
    version="1.0"
)


# 1. Create a Pydantic Model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None



# 2. Declare Model as Request Body
@app.post("/items/")
async def create_item(item: Item):
    total_price = item.price + (item.tax or 0)
    return {"item": item, "total_price": total_price}



# 3. Request Body + Path Parameter
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated_item": item}


# 4. Request Body + Path + Query Parameters
@app.put("/users/{user_id}/items/")
async def update_user_item(
    user_id: int,
    item: Item,
    notify: bool = Query(default=True, description="Send notification to user")
):
    return {
        "user_id": user_id,
        "notify_user": notify,
        "item": item
    }


