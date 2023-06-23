import pickle
from typing import Optional

from sqlalchemy.orm import Session

from src.database.db import client_redis
from src.database.models import User


async def get_user(name: str, db: Session) -> Optional[User]:
    if name is None:
        return

    user_byte = await client_redis.get(name)
    if user_byte:
        user = pickle.loads(user_byte)
        print("redis")
    else:
        user = db.query(User).filter_by(name=name).first()
    return user
