from fastapi import FastAPI
from enum import Enum
from typing import Union

app = FastAPI()

class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.get("/items/{item_id}")
async def read_item(
    item_id: str, 
    q: Union[str, None] = None,
    short: bool = False
):
    item = {"item_id": item_id}

    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})

    return {"item_id": item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learnging FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_pash:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/")
async def read_item(skip: int=0, limit: int=10):
    fake_items_db = [
        {"item_name": "Foo"},
        {"item_name": "Bar"},
        {"item_item": "Baz"}
    ]

    return fake_items_db[skip: skip + limit]
