from oauth import db
from oauth.models.base import Basemodel
from oauth.utils import generate_verification_token

class Users(Basemodel):
    google_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    token = db.Column(db.String(100), nullable=True)
    
    def __init__(self, google_id, name, email):
        super().__init__()
        self.google_id = google_id
        self.name = name
        self.email = email
        self.token = generate_verification_token(self.id)
        
