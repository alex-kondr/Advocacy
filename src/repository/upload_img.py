from uuid import uuid4

from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
import cloudinary.api

from src.conf.config import settings


cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)


def upload_img(file: UploadFile) -> str:
    public_id = f"Advocacy/{uuid4().hex}"
    cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    image_info = cloudinary.api.resource(public_id)
    src_url = image_info['secure_url']
    return src_url
