from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn

from src.database.db import get_db
from src.database.models import User
from src.repository.content import get_news
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
    content = await get_news(db)

    name = ''
    print(f"{token=}")
    if token:
        name = await auth_service.get_current_user(token, db)
    return templates.TemplateResponse("news.html", {
        "request": request,
        "content": content,
        "name": name
    })


@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post('/login')
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user = await db.query(User).filter_by(name=body.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid name")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token: str = await auth_service.create_access_token(data={'sub': user.name})
    return {'access_token': access_token, 'token_type': 'bearer'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
