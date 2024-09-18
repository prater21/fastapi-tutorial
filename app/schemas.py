from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


# ---------------------------------------------------------
# user model
class UserBase(BaseModel):
    email: EmailStr
    password: str


class CreateUser(UserBase):
    pass


class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    reg_time: datetime

    class Config:
        from_attributes = True


class LoginBase(BaseModel):
    email: EmailStr
    password: str


# ---------------------------------------------------------
# post model
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = Field(default=True)


class CreatePost(PostBase):
    pass


class ResponsePost(PostBase):
    id: int
    reg_time: datetime
    user_id: int
    user: ResponseUser

    class Config:
        from_attributes = True


class ResponsePosts(BaseModel):
    post: ResponsePost
    like: int

    class Config:
        from_attributes = True


# -----------------------------------------
# token model
class TokenBase(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# ---------------------------------------------
# like model
class LikeBase(BaseModel):
    post_id: int
    flag: bool  # True = like False = unlike
