from oauth import db
from oauth.models.base import Basemodel

class Users(Basemodel):
    __tablename__ = "users"
    account_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    github_access_token = db.Column(db.String(100))
    
    def __init__(self, account_id, name, email):
        super().__init__()
        self.account_id = account_id
        self.name = name
        self.email = email
