# docsについて作成

from fastapi import FastAPI, Query, Path, Body, Cookie
from enum import Enum
from typing import Union, List
from pydantic import BaseModel, Field
from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID


app = FastAPI()


@app.get("/items/{item_id:path}")
async def read_items1(
    item_id: int,
    skip: int = 0,
    limit: int = 10,
    q: Union[str, None] = None,
    short: bool = False
):
    return {"item_id": item_id, "skip": skip + limit}


# プルダウン用
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnel = "resnel"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.get("/items1/")
async def read_items2(
    q: Union[List[str], None] = Query(default=["foo", "bar"])
):
    query_items = {"q": q}
    return query_items


@app.post("/items2/")
async def create_item(item: Item):
    return item


@app.post("/items3/")
async def read_items3(
    q: Union[str, None] = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^fixedquery$",
        description="descriptionの記載",
        deprecated=True
    )
):
    results = {"items": [
        {"item_id": "Foo"},
        {"item_id": "Bar"}
    ]}

    if q:
        results.update({"q": q})

    return results


@app.get("/items2/{item_id}")
async def read_items2_id(
    q: str,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.put("/items3/{item_id}")
async def read_items3_id(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: Union[time, None] = Body(default=None)
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    };



