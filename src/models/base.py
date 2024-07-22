from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr


def get_str_uuid4():
    return str(uuid.uuid4())


@as_declarative()
class AbstractDefaultModel:
    id = Column(
        String(36),
        primary_key=True,
        unique=True,
        index=True,
        default=get_str_uuid4)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

    def to_dict(self, fields: list[str] | None = None) -> dict:
        data = self.__dict__.copy()

        if fields is not None:
            for field in fields:
                data[field] = getattr(self, field, None)

        del data['_sa_instance_state']
        return data

    def __repr__(self):
        return f'{self.__class__.__name__} {self.id}'
