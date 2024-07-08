from fastapi import FastAPI, Query, Path, Body
from enum import Enum
from typing import Union
from pydantic import BaseModel


app = FastAPI()


# 引数等の値の選択用
class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


# リクエストボディの送付check用
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/items/{item_id}")
async def read_item(
    q: Union[str, None] = None,
    short: bool = False,
    # PathはURLパスの一部、Queryは/?~の?以降のもの
    item_id: int = Path(
        title="The ID of the item to get",
        ge=1,
        le=1000
    ),
    size: float = Query(gt=0, lt=10.5),
):
    item = {"item_id": item_id}

    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})

    return {"item_id": item_id}


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body()):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


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
async def read_item(
    skip: int=0,
    limit: int=10,
    q: Union[str, None] = Query(
        default=None,
        min_length=3,
        max_length=10,
        description="説明",
        deprecated=True)
):
    fake_items_db = [
        {"item_name": "Foo"},
        {"item_name": "Bar"},
        {"item_item": "Baz"}
    ]

    return str(fake_items_db[skip: skip + limit]) + q


@app.post("/items2/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    print(item_dict)
    return item_dict
