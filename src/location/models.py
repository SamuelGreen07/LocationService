from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, JSON, Integer, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from models.base import AbstractDefaultModel
import uuid


class Task(AbstractDefaultModel):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String, nullable=False)
    data = Column(JSON, nullable=True)


class Point(AbstractDefaultModel):
    __tablename__ = 'points'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
