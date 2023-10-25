from uuid import uuid4
from datetime import datetime
from oauth import db
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


def get_uuid():
    """generate a unique id
    """
    return uuid4().hex

Base = declarative_base()
class Basemodel(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=get_uuid, unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
        
    @property
    def formatted_created_at(self):
        # Format the timestamp when accessed
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    @property
    def formatted_updated_at(self):
        # Format the timestamp when accessed
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
