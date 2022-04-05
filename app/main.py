from datetime import datetime
from math import prod
from multiprocessing import synchronize
from statistics import mode
from sys import prefix
import utils
from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from typing import List
import models, schemas
from models import Product
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from loguru import logger

from routers import user, product

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user.router)
app.include_router(product.router)