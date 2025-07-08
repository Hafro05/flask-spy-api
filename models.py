from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    os = db.Column(db.String(100))
    browser = db.Column(db.String(100))
    user_agent = db.Column(db.Text)
    ville = db.Column(db.String(100))
    prediction = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
