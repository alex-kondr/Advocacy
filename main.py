from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.routes import auth, contacts


app_dir = Path(__file__).parent

app = FastAPI()
app.mount("/src/routes/static", StaticFiles(directory="src/routes/static"), name="routes_static")
app.mount("/src/routes/img", StaticFiles(directory="src/routes/img"), name="routes_img")
templates = Jinja2Templates(directory=app_dir / "src/routes/templates")

app.include_router(auth.router)
app.include_router(contacts.router)

@app.get('/')
def hello(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)