from datetime import datetime
from turtle import update
from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: int
    price: str
    stock: str
    description: str

class ProductUpdate(ProductCreate):
    isDeleted: bool = False
    isAvailable: bool = True
    updated_at: datetime = datetime.now()

class ResponseProduct(BaseModel):
    name: str
    category: int
    price: str
    stock: str
    description: str
    thumbnail: Optional[str] = None
    isDeleted: bool
    isAvailable: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
