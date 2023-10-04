from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

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
