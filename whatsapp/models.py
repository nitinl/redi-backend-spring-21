from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(40), unique=True, nullable=False)
    status = db.Column(db.String(80))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    primary_user_rel = db.relationship('User', foreign_keys='Contact.primary_user')
    contact_user_rel = db.relationship('User', foreign_keys='Contact.contact_user')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_rel = db.relationship('User', foreign_keys='Message.sender')
    receiver_rel = db.relationship('User', foreign_keys='Message.receiver')
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'text': self.text,
            'timestamp': self.timestamp,
            'sender': self.sender_rel.username,
            'receiver': self.receiver_rel.username,
        }
