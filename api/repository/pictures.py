from typing import List
from faker import Faker
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from api.conf.config import settings
from api.database.models import Picture, User, Tag
from api.schemas import PictureCreate, PictureBase


async def create_picture(body: PictureCreate, file_path: str, db: Session):

    tags_list = transformation_list_to_tag(body.tags, db)
    picture = Picture(picture_url=file_path, description=body.description, tags=tags_list)
    db.add(picture)
    db.commit()
    db.refresh(picture)
    # , user_id = user.id
    return picture


def get_tag_by_name(tag_name: str, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    return tag


def transformation_list_to_tag(tags: list, db: Session) -> List[Tag]:
    # , user
    list_tags = []
    if tags:
        for tag_name in tags:
            tag = get_tag_by_name(tag_name, db)
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
                # user,
            list_tags.append(tag)
    return list_tags


async def get_picture(picture_id: int, db: Session) -> Picture | None:
    picture = db.query(Picture).filter(Picture.id == picture_id).first()
    return picture


async def get_user_pictures(user_id: int, db: Session) -> List[Picture]:

    pictures = db.query(Picture).filter(Picture.user_id == user_id).all()
    return pictures


async def remove_picture(picture_id: int, db: Session):

    picture = db.query(Picture).filter(Picture.id == picture_id).first()
    if picture:
        db.delete(picture)
        db.commit()
    return picture


async def update_picture(picture_id: int, body: PictureCreate, db: Session):
    # , user: User
    picture = db.query(Picture).filter(Picture.id == picture_id).first()

    if picture:
        tags_list = transformation_list_to_tag(body.tags, db)
        # user,
        picture.description = body.description
        picture.tags = tags_list
        db.commit()
        db.refresh(picture)
    return picture

