from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from jose import jwt
from enum import Enum
from typing import Optional

class Type(Enum):
    hardware = "hardware"
    software = "software"

class Item(BaseModel):
    name: str
    type: Type
    price: int = Field(100, gt=0, lt=2500, description="The price of the item")

class ResponseItem(BaseModel):
    id: int
    name: str
    type: Type
    price: int

items = [
    Item(name="PC", type="hardware", price=1000),
    Item(name="Mac", type="hardware", price=1500),
    Item(name="Monitor", type="hardware", price=500),
    Item(name="Win", type="software", price=150),
    Item(name="Linux", type="software", price=1),
    Item(name="Doom", type="software", price=50)
]

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

@app.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()) -> dict:
    if data.username == "admin" and data.password == "admin":
        access_token = jwt.encode({ "user": data.username }, key="secret", algorithm="HS256")
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )

@app.get("/items/")
async def get_items(token: str = Depends(oauth2_schema), type: Optional[str] = None) -> list:
    username = jwt.decode(token, key="secret", algorithms=["HS256"])["user"]
    if type:
        data = []
        for item in items:
            if item.type.value == type:
                data.append(item)
        return data
    return items

@app.get("/items/{item_id}", dependencies=[Depends(oauth2_schema)])
async def get_item(item_id: int) -> Item:
    return items[item_id]

@app.post("/items/", response_model=ResponseItem, dependencies=[Depends(oauth2_schema)])
async def create_item(data: Item):
    items.append(data)
    response_data = ResponseItem(id=len(items)-1, name=data.name, type=data.type, price=data.price)
    return response_data

@app.put("/items/{item_id}", response_model=ResponseItem, dependencies=[Depends(oauth2_schema)])
async def update_item(item_id: int, data:Item):
    items[item_id] = data
    response_data = ResponseItem(id=item_id, name=data.name, type=data.type, price=data.price)
    return response_data

@app.delete("/items/{item_id}", dependencies=[Depends(oauth2_schema)])
async def delete_item(item_id: int) -> dict[str, Item]:
    item = items[item_id]
    items.pop(item_id)
    return {"deleted_item": item}
