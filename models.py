# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ScheduledEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, default=False)
