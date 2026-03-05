from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI(
    title="FastAPI Query Parameters Demo",
    description="Demonstrates important concepts of query parameters",
    version="1.0"
)


# 1. Default query parameters
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {
        "message": "Default Query Parameters Example",
        "skip": skip,
        "limit": limit
    }


# 2. Optional Query Parameters
@app.get("/products/")
async def read_products(search: Optional[str] = None):
    if search:
        return {"message": f"Searching for product: {search}"}

    return {"message": "No search query provided"}



# 3. Query Parameter Type Conversion
@app.get("/orders/")
async def get_orders(limit: int = 10, active: bool = True):
    return {
        "limit": limit,
        "active": active
    }


# 4. Multiple Path and Query Parameters
@app.get("/users/{user_id}/items/")
async def get_user_items(user_id: int, skip: int = 0, limit: int = 5):
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit
    }


# 5. Required Query Parameter
@app.get("/search/")
async def search_items(keyword: str = Query(..., description="Keyword to search items")):
    return {
        "message": "Search results",
        "keyword": keyword
    }



# Example Endpoint Demonstrating Multiple Concepts
@app.get("/filter/")
async def filter_items(
    category: Optional[str] = None,
    min_price: float = 0,
    max_price: float = 1000,
    available: bool = True
):
    return {
        "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "available": available
    }

