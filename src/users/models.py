from sqlalchemy import Column, String, Index

from models.base import AbstractDefaultModel


class User(AbstractDefaultModel):
    __tablename__ = 'users'

    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
