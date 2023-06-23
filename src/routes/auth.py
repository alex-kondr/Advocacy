import pickle
from pathlib import Path
from typing import Optional

from fastapi import Request, Depends, HTTPException, status, APIRouter, Query
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from psycopg2 import OperationalError
from sqlalchemy.orm import Session

from src.database.db import get_db, client_redis
from src.database.models import User
from src.repository import user as repository_user
from src.repository.auth import auth_service


app_dir = Path(__file__).parent.parent
router = APIRouter(prefix="/login")

router.mount("/src/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory=app_dir / "templates")


@router.get('/')
async def login(request: Request,
                token: Optional[str] = Query(default=None),
                db: Session = Depends(get_db)
                ):

    try:
        if await auth_service.get_current_user(token, db):
            return RedirectResponse(f"/news?token={token}")

    except OperationalError as err:
        print(err)

    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/')
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user: User = await repository_user.get_user(body.username, db)

    if user is None or not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не вірний логін або пароль")

    await client_redis.set(body.username, pickle.dumps(user), ex=86400)
    access_token: str = await auth_service.create_access_token(data={'sub': user.name})
    return {'access_token': access_token, 'token_type': 'bearer'}
