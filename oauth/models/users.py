from oauth import db
from oauth.models.base import Basemodel, Base


class Users(Basemodel, Base):

    __tablename__ = "users"

    account_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    avatar = db.Column(db.String(255))

    def __init__(self, account_id, name, email, avatar):
        super().__init__()
        self.account_id = account_id
        self.name = name
        self.email = email
        self.avatar = avatar
