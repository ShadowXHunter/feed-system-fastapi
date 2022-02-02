from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException,status
from fastapi.encoders import jsonable_encoder

def get_all(db: Session):
    feed = db.query(models.Feed).all()
    return feed

def create(request: schemas.Feed,db: Session, username:str):
    userid = db.query(models.User).filter(models.User.username == username).first().id
    new_message = models.Feed(message=request.message,user_id=userid)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def destroy(id:int,db: Session, username:str):
    message = db.query(models.Feed).filter(models.Feed.id == id)

    if not message.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Message with id {id} not found")
    if not message.first().creator.username == username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not the creator of message with id {id}.")

    message.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id:int,request:schemas.Feed, db:Session, username:str):
    message = db.query(models.Feed).filter(models.Feed.id == id)

    if not message.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Message with id {id} not found")
    if not message.first().creator.username == username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not the creator of message with id {id}.")

    
    message.update(request.dict())
    db.commit()
    return 'updated'

def show(id:int,db:Session):
    message = db.query(models.Feed).filter(models.Feed.id == id).first()
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Message with the id {id} is not available")
    return message