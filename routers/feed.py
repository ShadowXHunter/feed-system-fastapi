from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from repository import feed

router = APIRouter(
    prefix="/feed",
    tags=['Feed']
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowMessage])
def all(db: Session = Depends(get_db), username: str = Depends(oauth2.get_current_user)):
    return feed.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Feed, db: Session = Depends(get_db), username: str = Depends(oauth2.get_current_user)):
    return feed.create(request, db, username)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db), username: str = Depends(oauth2.get_current_user)):
    return feed.destroy(id,db, username)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Feed, db: Session = Depends(get_db), username: str = Depends(oauth2.get_current_user)):
    return feed.update(id,request, db, username)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowMessage)
def show(id:int, db: Session = Depends(get_db), username: str = Depends(oauth2.get_current_user)):
    return feed.show(id,db)


