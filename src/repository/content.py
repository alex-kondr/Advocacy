from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.database.models import Content


async def get_news(db: Session, limit: int = 10) -> list:
    return db.query(Content).order_by(desc(Content.created_at)).limit(limit).all()


async def add_news(db: Session, title: str = None, body: str = None, url=None):
    news = Content(img=url, title=title, body=body)
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


async def delete_news(news_id: int, db: Session):
    db.query(Content).filter_by(id=news_id).delete()
    db.commit()
