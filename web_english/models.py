from web_english import db
from datetime import datetime


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    text_eu = db.Column(db.Text, unique=True, nullable=False)
    text_ru = db.Column(db.Text, unique=True, nullable=False)
    published = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    duration = db.Column(db.Integer)

    def __repr__(self):
        return f"<Content {self.title}>"
        