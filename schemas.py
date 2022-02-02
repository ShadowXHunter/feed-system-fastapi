from typing import List, Optional
from pydantic import BaseModel


class FeedBase(BaseModel):
    message: str

class Feed(FeedBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    username:str
    email:str
    password:str

class ShowUser(BaseModel):
    username:str
    email:str
    messages : List[Feed] =[]
    
    class Config():
        orm_mode = True

class CreatorName(BaseModel):
    username:str
    
    class Config():
        orm_mode = True

class ShowMessage(BaseModel):
    message:str
    creator: CreatorName

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None