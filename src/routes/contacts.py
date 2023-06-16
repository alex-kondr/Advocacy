from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/contacts", tags=["contacts"])

app_dir = Path(__file__).parent
templates = Jinja2Templates(directory=app_dir / "templates")


@router.get("/create_contact")
def create_contact(request: Request):
    return templates.TemplateResponse("create_contact.html", {"request": request})


@router.get("/edit_contact")
def edit_contact(request: Request):
    return templates.TemplateResponse("edit_contact.html", {"request": request})


@router.get("/edit_avatar")
def edit_contact(request: Request):
    return templates.TemplateResponse("edit_avatar.html", {"request": request})


@router.get("/")
def get_contacts(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})