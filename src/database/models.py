from sqlalchemy import Enum

from sqlalchemy import Boolean, Column, Date, Integer, String, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

default_img = "https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-for-website-design-or-mobile-app-no-photo-available_87543-11093.jpg?w=996"


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=True)
    body = Column(String(255), nullable=True, default=None)
    img = Column(String(255), nullable=True, default=default_img)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
