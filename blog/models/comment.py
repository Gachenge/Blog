from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from blog import db
from blog.models.base import Basemodel, Base

class Comment(Basemodel, Base):
    __tablename__ = "comments"

    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.String(60), db.ForeignKey('posts.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(255))

    user = relationship("Users")  # Define a relationship to the User model
    post = relationship("Posts")  # Define a relationship to the Post model

    def __init__(self, user_id, post_id, text, image_url):
        super().__init__()
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.image_url = image_url
