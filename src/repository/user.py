from typing import Optional

from sqlalchemy.orm import Session

from src.database.db import client_redis
from src.database.models import User


async def get_user(name: str, db: Session) -> Optional[User]:
    user = await client_redis.get(name)
    if user is None:
        user = db.query(User).filter_by(name=name).first()
    return user
