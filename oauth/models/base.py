from uuid import uuid4
from datetime import datetime
from oauth import db
from sqlalchemy import Column, Integer, DateTime


def get_uuid():
    """generate a unique id
    """
    return uuid4().hex

class Basemodel(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=get_uuid, unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
