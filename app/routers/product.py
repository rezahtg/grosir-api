from fastapi import HTTPException, status, Depends, APIRouter
from database import get_db
from loguru import logger
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, select
import models,schemas

router = APIRouter(
    prefix='/api/v1/products'
)

@router.get('/', response_model=List[schemas.ResponseProduct], tags=['Products Service'])
async def getAllProduct(db: Session = Depends(get_db)):
    startTime = datetime.now()
    logsId = startTime.strftime("%y%m%d%H%M%S%f")
    try:
        products = db.query(models.Product).all()
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Error Querying Database')

    logger.info('{0}| Querying Database: {1}'.format(logsId, products))
    endTime = datetime.now()
    timeDelta = endTime - startTime
    logger.info('{0}| Process finished. Time elapsed: '.format(logsId) + str(timeDelta.total_seconds()*1000) + 'ms') 

    return products

@router.get('/{name}', response_model=schemas.ResponseProduct, tags=['Products Service'])
def getProductByName(productName:str, db: Session = Depends(get_db)):
    startTime = datetime.now()
    logsId = startTime.strftime("%y%m%d%H%M%S%f")

    try:
        products = db.query(models.Product).filter(func.lower(models.Product.name) == func.lower(productName)).first()
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Error Querying Database')

    logger.info('{0}| Querying Database: {1}'.format(logsId, products))
    endTime = datetime.now()
    timeDelta = endTime - startTime
    logger.info('{0}| Process finished. Time elapsed: '.format(logsId) + str(timeDelta.total_seconds()*1000) + 'ms') 

    return products

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseProduct, tags=['Products Service'])
def createProduct(req: schemas.ProductCreate, db: Session = Depends(get_db) ):
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

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ResponseProduct, tags=['Products Service'])
def updateProduct(req: schemas.ProductUpdate, id:int, db: Session = Depends(get_db)):
    startTime = datetime.now()
    logsId = startTime.strftime("%y%m%dH%M%S%f")
    product = ''
    
    try:
        product_query = db.query(models.Product).filter(models.Product.id == id)
        product = product_query.first()
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Error Querying Database')

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product with ID {0} does not exist'.format(id))               

    product_query.update(req.dict(), synchronize_session=False)
    db.commit()
    
    res = product_query.first()

    endTime = datetime.now()
    timeDelta = endTime - startTime
    logger.info('{0}| Process finished. Time elapsed: '.format(logsId) + str(timeDelta.total_seconds()*1000) + 'ms')

    return res


# Hard delete product
@router.delete('/products/{id}', status_code=status.HTTP_200_OK, tags=['Products Service'])
def deletePost(id: int, db: Session = Depends(get_db)):
    startTime = datetime.now()
    logsId = startTime.strftime("%y%m%dH%M%S%f")
    product = ''

    try:
        product_query = db.query(models.Product).filter(models.Product.id == id)
        product = product_query.first()
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Error Querying')
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product with ID {0} does not exist'.format(id))
    
    product_query.delete(synchronize_session=False)
    db.commit()

    endTime = datetime.now()
    timeDelta = endTime - startTime
    logger.info('{0}| Process finished. Time elapsed: '.format(logsId) + str(timeDelta.total_seconds()*1000) + 'ms')

    return 'Data successfully deleted!'