from typing import Optional
from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.database.models import User
from src.database.db import get_db
from src.conf.config import settings
from src.repository import user as repository_user


class Auth:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    SECRET_KEY = settings.secret_key
    ALGORITHM = "HS256"
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(weeks=1)

        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'access_token'})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    def verify_access_token(self, token: str = Depends(oauth2_scheme)) -> str:
        name = None
        try:
            payload = jwt.decode(token or "", self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get('scope') == 'access_token':
                name = payload.get('sub')
        except JWTError as err:
            print(err)
        return name

    async def get_current_user(self, token: str = Depends(oauth2_scheme),
                               db: Session = Depends(get_db)) -> Optional[User]:
        name = self.verify_access_token(token)
        user = await repository_user.get_user(name, db)
        return user


auth_service = Auth()
