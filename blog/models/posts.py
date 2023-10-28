from blog import db
from blog.models.base import Basemodel, Base
from sqlalchemy.orm import relationship


class Posts(Basemodel, Base):

    __tablename__ = "posts"

    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    image_url = db.Column(db.String(255))

    user = relationship("Users")

    def __init__(self, user_id, body, image_url):
        super().__init__()
        self.user_id = user_id
        self.body = body
        self.image_url = image_url
