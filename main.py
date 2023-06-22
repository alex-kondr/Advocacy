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
from src.routes import content
from src.routes import auth


app_dir = Path(__file__).parent

app = FastAPI()
app.include_router(content.router)
app.include_router(auth.router)

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory=app_dir / "src/templates")


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
