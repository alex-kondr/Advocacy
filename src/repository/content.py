from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.database.models import Content


async def get_news(db: Session, limit: int=10) -> list:
    return db.query(Content).order_by(desc(Content.created_at)).limit(limit).all()