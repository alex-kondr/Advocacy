from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository.content import get_news


app_dir = Path(__file__).parent

app = FastAPI()
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory=app_dir / "src/templates")


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/news')
async def index_test(request: Request, db: Session = Depends(get_db)):
    content = await get_news(db)
    return templates.TemplateResponse("news.html", {"request": request, "content": content})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)