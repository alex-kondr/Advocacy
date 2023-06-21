from pathlib import Path
from typing import Optional, Union, Annotated

from fastapi import FastAPI, Request, Depends, HTTPException, status, Query, File, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
from psycopg2 import OperationalError, Error

from src.database.db import get_db
from src.database.models import User
from src.repository import content as repository_content
from src.repository.upload_img import upload_img
from src.repository.auth import auth_service


app_dir = Path(__file__).parent

app = FastAPI()
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory=app_dir / "src/templates")


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/news')
async def news(request: Request, token: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    invalid_token = False
    name = ''
    content = None

    try:
        content = await repository_content.get_news(db)

        if token:
            name = await auth_service.get_current_user(token, db)
            if not name:
                invalid_token = True

    except:
        invalid_token = True

    return templates.TemplateResponse("news.html", {
        "request": request,
        "content": content,
        "name": name,
        "invalid_token": invalid_token
    })


@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get('/add_news')
async def add_news(request: Request):
    return templates.TemplateResponse("add_news.html", {"request": request})


@app.post('/add_news')
async def add_news(
        request: Request,
        token: Optional[str] = Query(default=None),
        title: Annotated[str, Form()] = None,
        body: Annotated[str, Form()] = None,
        file: Union[UploadFile, None] = None,
        db: Session = Depends(get_db)

):
    message = ""

    try:

        if token and await auth_service.get_current_user(token, db) and (title or body or file):
            url = upload_img(file) if file.filename else None
            await repository_content.add_news(db, title, body, url=url)
        else:
            message = "Потрібно залогінитись"
        print(f"{message=}")

    except OperationalError as err:
        print(err)
    # return templates.TemplateResponse("news.html", {"request": request})


@app.post('/login')
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter_by(name=body.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не вірний логін")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не вірний пароль")

    access_token: str = await auth_service.create_access_token(data={'sub': user.name})
    return {'access_token': access_token, 'token_type': 'bearer'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
