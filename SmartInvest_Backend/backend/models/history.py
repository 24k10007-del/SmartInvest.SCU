from database import db
from datetime import datetime


class History(db.Model):

    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)

    symbol = db.Column(db.String(20))

    price = db.Column(db.Float)

    recommendation = db.Column(db.String(20))

    score = db.Column(db.Integer)

    confidence = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)