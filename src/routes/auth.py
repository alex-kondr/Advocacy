from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/auth", tags=["auth"])

app_dir = Path(__file__).parent
templates = Jinja2Templates(directory=app_dir / "templates")


@router.get("/singin")
def form(request: Request):
    return templates.TemplateResponse("singin.html", {"request": request})


@router.get("/singup")
def form(request: Request):
    return templates.TemplateResponse("singup.html", {"request": request})