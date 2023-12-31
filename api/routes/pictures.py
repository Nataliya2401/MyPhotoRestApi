from typing import List
from faker import Faker
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from api.conf.config import settings
from api.schemas import PictureBase, PictureResponse, PictureCreate

from api.servises.cloud_picture import CloudImage

from api.database.db import get_db
from api.database.models import User
from api.repository import pictures as repository_pictures

# from api.repository import users as repository_users
# from api.services.auth import auth_service
# from api.schemas import UserResponse

router = APIRouter(prefix='/pictures', tags=["pictures"])


@router.post("/", response_model=PictureResponse, status_code=status.HTTP_201_CREATED)
async def create_picture(body: PictureCreate, file: UploadFile = File(None), db: Session = Depends(get_db)):
    #
    public_id = Faker().first_name().lower()
    r = CloudImage.upload(file.file, public_id)
    picture_url = CloudImage.get_url_for_picture(public_id, r)
    return await repository_pictures.create_picture(body, picture_url, db)


@router.post("/new2")
async def root(file: UploadFile = File(None)):
    # f,, response_model=PictureResponse, status_code=status.HTTP_201_CREATED
    public_id = Faker().first_name().lower()
    r = CloudImage.upload(file.file, public_id)
    picture_url = CloudImage.get_url_for_picture(public_id, r)

    print(picture_url, "223241")

    return {"file_name": file.filename}


@router.post("/new", response_model=PictureResponse, status_code=status.HTTP_201_CREATED)
async def create_picture(body: PictureCreate, db: Session = Depends(get_db)):
    public_id = Faker().first_name().lower()
    return await repository_pictures.create_picture(body, public_id, db)


@router.get("/{picture_id}", response_model=PictureResponse)
async def get_picture(picture_id: int, db: Session = Depends(get_db)):
    picture = await repository_pictures.get_picture(picture_id, db)
    if picture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return picture


@router.put("/{picture_id}", response_model=PictureResponse)
async def update_photo(body: PictureCreate, picture_id: int, db: Session = Depends(get_db)):
    picture = await repository_pictures.update_picture(picture_id, body, db)
    if picture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture not found")
    return picture


@router.delete("/{picture_id}", response_model=PictureResponse)
async def remove_picture(picture_id: int, db: Session = Depends(get_db)):
    picture = await repository_pictures.remove_picture(picture_id, db)
    if picture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture not found")
    return picture

