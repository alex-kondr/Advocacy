from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn


app_dir = Path(__file__).parent

app = FastAPI()
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")
app.mount("/123", StaticFiles(directory="123"), name="nicepage")
templates = Jinja2Templates(directory=app_dir / "src/templates")
test = Jinja2Templates(directory=app_dir / "123")


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/test')
def index_test(request: Request):
    return test.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)