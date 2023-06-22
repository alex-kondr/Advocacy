from pathlib import Path
from typing import Optional, Union, Annotated

from fastapi import FastAPI, Request, Depends, HTTPException, status, Query, File, UploadFile, Form, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from psycopg2 import OperationalError

from src.database.db import get_db
from src.database.models import User
from src.repository import content as repository_content
from src.repository.upload_img import upload_img
from src.repository.auth import auth_service

app_dir = Path(__file__).parent.parent
router = APIRouter(prefix='/news', tags=['news'])

router.mount("/src/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory=app_dir / "templates")


@router.get('/add')
async def add_news(request: Request):
    return templates.TemplateResponse("add_news.html", {"request": request})


@router.post('/add')
async def add_news(
        request: Request,
        title: Annotated[str, Form()],
        body: Annotated[str, Form()],
        token: Optional[str] = Query(default=None),
        file: Union[UploadFile, None] = None,
        db: Session = Depends(get_db)

):
    message = ""
    print(f"{token=}")
    print(f"{title=}")
    print(f"{body=}")

    try:
        if token and await auth_service.get_current_user(token, db) and (title or body or file):
            url = upload_img(file) if file.filename else None
            await repository_content.add_news(db, title, body, url)
        else:
            message = "Потрібно залогінитись"
        print(f"{message=}")

    except OperationalError as err:
        print(err)
    # return RedirectResponse("/news")


@router.get('/')
async def news(request: Request, token: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    invalid_token = False
    user = None
    content = None

    try:
        content = await repository_content.get_news(db)

        if token:
            user = await auth_service.get_current_user(token, db)
            if not user:
                invalid_token = True
                # print("except")

    except:
        invalid_token = True
        print("except")

    # print(f"{content=}")
    # print(f"{user=}")
    # print(f"{invalid_token=}")

    return templates.TemplateResponse("news.html", {
        "request": request,
        "content": content,
        "name": user,
        "invalid_token": invalid_token
    })
