import pickle
from pathlib import Path
from typing import Optional, Union, Annotated

from fastapi import FastAPI, Request, Depends, HTTPException, status, Query, File, UploadFile, Form, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
from psycopg2 import OperationalError, Error

from src.database.db import get_db, client_redis
from src.database.models import User
from src.repository import content as repository_content
from src.repository.upload_img import upload_img
from src.repository.auth import auth_service


app_dir = Path(__file__).parent.parent
router = APIRouter(prefix="/login")

router.mount("/src/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory=app_dir / "templates")


@router.get('/')
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/')
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter_by(name=body.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не вірний логін")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не вірний пароль")

    await client_redis.set(body.username, pickle.dumps(user), ex=7200)
    access_token: str = await auth_service.create_access_token(data={'sub': user.name})
    return {'access_token': access_token, 'token_type': 'bearer'}