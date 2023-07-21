from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

from src.database.models import Role


class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    detail: str = "User successfully created"
    roles: Role

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    photo_url: str
    description: Optional[str]
    tags: Optional[List[TagModel]]


class PhotoModel(PhotoBase):
    tags: List[int]


class PhotoUpdate(PhotoModel):
    update: bool


class PhotoStatusUpdate(BaseModel):
    update: bool


class PhotoResponse(PhotoBase):
    id: int
    created_at: datetime
    tags: Optional[List[TagResponse]]

    class Config:
        orm_mode = True


class CommentModel(BaseModel):
    comment_text: str = Field("comment_text")


class CommentResponse(BaseModel):
    id: int
    comment_text: Optional[str]
    created_at: datetime
    updated_at: Optional[date] = None
    user_id: int

    class Config:
        orm_mode = True


