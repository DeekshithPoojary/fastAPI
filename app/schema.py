from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class postBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None


class postCreate(postBase):
    pass


class userOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(postBase):  #BaseModel
    id: int
    #title: str
    #content: str
    #published: bool
    create_at: datetime
    owner_id: int
    owner : userOut  #this will fetch owner details along id

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class userCreate(BaseModel):
    email: EmailStr
    password: str


class userLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class token_data(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore