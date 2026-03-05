from fastapi import FastAPI, Path
from enum import Enum
from pydantic import BaseModel


app = FastAPI(
    title="FastAPI Path Parameters Demo",
    description="Demonstrates all major path parameter concepts",
    version="1.0"
)

# Pydantic Model
class Item(BaseModel):
    id: int
    name: str
    price: float

#fake_db
items_db = {
    1: {"name": "Laptop", "price": 1200},
    2: {"name": "Phone", "price": 800},
    3: {"name": "Keyboard", "price": 100}
}


# 1. Path Parameters with Data Types
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}



# 2. Data Validation with Path()
@app.get("/products/{product_id}")
async def get_product(
    product_id: int = Path(
        title="Product ID",
        description="The ID of the product you want to retrieve",
        gt=0,
        le=1000
    )
):
    """
    Path() allows validation rules.
    Here product_id must be:
    > 0 and <= 1000
    """
    return {"product_id": product_id}



# 3. Order
@app.get("/users/me")
async def read_current_user():
    return {"user": "current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


# 4. Predefined Values using Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    
    # Compare enumeration members
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "AlexNet selected"}

    if model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "LeNet selected"}

    # Get enum value
    if model_name.value == "resnet":
        return {"model_name": model_name, "message": "ResNet selected"}

    return {"model_name": model_name}



# 5. Returning Enumeration Members
@app.get("/model-info/{model_name}")
async def model_info(model_name: ModelName):
    return {"model": model_name}



# 6. Using Path Parameters with Database Example
@app.get("/store/items/{item_id}")
async def read_store_item(item_id: int):
    if item_id not in items_db:
        return {"error": "Item not found"}
    return {"item_id": item_id, "data": items_db[item_id]}



# 7. Path Parameters Containing Paths
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

