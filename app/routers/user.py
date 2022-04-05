from fastapi import HTTPException, status, Depends, APIRouter
import models,schemas, utils
from database import get_db
from loguru import logger
from datetime import datetime

from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/api/v1/users',
    tags=['User Services']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.userResponseModel)
def createUsert(req: schemas.UserCreate, db: Session = Depends(get_db) ):
    startTime = datetime.now()
    logsId = startTime.strftime("%y%m%d%H%M%S%f")

    #hashing password user
    hashedPassword = utils.hash(req.password)
    req.password = hashedPassword
    res = models.User(**req.dict())

    db.add(res)
    db.commit()
    db.refresh(res)

    endTime = datetime.now()
    timeDelta = endTime - startTime
    logger.info('{0}| Process finished. Time elapsed: '.format(logsId) + str(timeDelta.total_seconds()*1000) + 'ms')

    return res

@router.get('/{id}', response_model=schemas.userResponseModel)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with ID {0} does not exist')
    
    return user