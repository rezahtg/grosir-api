from datetime import datetime
from turtle import update
from pydantic import BaseModel, EmailStr
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

class ResponseProduct(ProductCreate):
    thumbnail: Optional[str] = None
    isDeleted: bool
    isAvailable: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str

class userResponseModel(BaseModel):
    full_name: str
    username: str
    email: EmailStr

    class Config:
        orm_mode=True