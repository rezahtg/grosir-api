from datetime import datetime
from unicodedata import category
from fastapi import FastAPI, Depends, HTTPException, status, Body
import psycopg2
import time
import models
from pydantic import BaseModel
from typing import Optional, Type
from models import Base, Product, RequestProduct
from database import engine, get_db
from sqlalchemy.orm import Session
from loguru import logger

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/products')
def getAllProduct(db: Session = Depends(get_db) ):
    startTime = datetime.now()
    logsId = startTime.strftime("%y%m%d%H%M%S%f")
    products = db.query(Product).all()

    logger.info('{0}| Querying Database: {1}'.format(logsId, products))
    endTime = datetime.now()
    timeDelta = endTime - startTime
    logger.info('{0}| Process finished. Time elapsed: '.format(logsId) + str(timeDelta.total_seconds()*1000) + 'ms') 

    return products

@app.post('/products', status_code=status.HTTP_201_CREATED)
def createProduct(req: RequestProduct, db: Session = Depends(get_db) ):
    startTime = datetime.now()
    logsId = startTime.strftime("%y%m%d%H%M%S%f")

    res = models.Product(**req.dict())

    db.add(res)
    db.commit()
    db.refresh(res)

    logger.info('{0}| Querying Database: {1}'.format(logsId, res))
    endTime = datetime.now()
    timeDelta = endTime - startTime
    logger.info('{0}| Process finished. Time elapsed: '.format(logsId) + str(timeDelta.total_seconds()*1000) + 'ms')

    return res