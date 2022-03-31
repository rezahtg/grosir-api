from email.policy import default
from typing import Collection
from unicodedata import category
from xmlrpc.client import Boolean
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(Integer, nullable=False)
    price = Column(String, nullable=False)
    stock = Column(String, nullable=True)
    description = Column(String,nullable=True)
    thumbnail = Column(String, nullable=True)
    isDeleted = Column(Boolean, server_default='FALSE', nullable=False)
    isAvailable = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)

class RequestProduct(BaseModel):
    name: str
    category: int
    price: str
    stock: str
    description: str