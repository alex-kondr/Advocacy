from pathlib import Path
from typing import Optional, Union, Annotated

from fastapi import Request, Depends, Query, UploadFile, Form, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from psycopg2 import OperationalError

from src.database.db import get_db
from src.repository import content as repository_content
from src.repository.upload_img import upload_img
from src.repository.auth import auth_service

app_dir = Path(__file__).parent.parent
router = APIRouter(prefix='/news', tags=['news'])

router.mount("/src/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory=app_dir / "templates")


@router.get('/add')
async def add_news(request: Request,
                   token: Optional[str] = Query(default=None),
                   db: Session = Depends(get_db)
                   ):
    message = None
    try:
        if not await auth_service.get_current_user(token, db):
            message = "Потрібно авторизуватись."

    except OperationalError as err:
        print(err)
        message = "Помилка підключення до бази даних."

    print(f"{message=}")

    return templates.TemplateResponse("add_news.html", {"request": request,
                                                        "message": message,
                                                        "token": token,
                                                        }
                                      )


@router.post('/add')
async def add_news(
        title: Annotated[str, Form()],
        body: Annotated[str, Form()],
        token: Optional[str] = Query(default=None),
        file: Union[UploadFile, None] = None,
        db: Session = Depends(get_db)

):

    try:
        if await auth_service.get_current_user(token, db):
            url = upload_img(file) if file.filename else None
            await repository_content.add_news(db, title, body, url)
        else:
            print("Потрібно залогінитись")

    except OperationalError as err:
        print(err)


@router.get('/')
async def news(request: Request, token: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    user = None
    contents = []

    try:
        contents = await repository_content.get_news(db)
        user = await auth_service.get_current_user(token, db)

    except OperationalError as err:
        print(err)

    return templates.TemplateResponse("news.html", {
        "request": request,
        "contents": contents,
        "authorize": True if user else False,
        "token": token
    })


@router.get('/{news_id}')
async def delete_news(news_id: int,
                   token: Optional[str] = Query(default=None),
                   db: Session = Depends(get_db)
                   ):
    try:
        if await auth_service.get_current_user(token, db):
            await repository_content.delete_news(news_id, db)
            return RedirectResponse(f"/news?token={token}")

    except OperationalError as err:
        print(err)
