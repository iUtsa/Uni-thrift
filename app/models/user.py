from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(120), default='default_profile.jpg')
    is_verified = db.Column(db.Boolean, default=False)
    university = db.Column(db.String(120))
    major = db.Column(db.String(120))
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='seller', lazy='dynamic')
    orders_as_buyer = db.relationship('Order', foreign_keys='Order.buyer_id', backref='buyer', lazy='dynamic')
    
    # We'll define these relationships after both models are defined
    # reviews_given and reviews_received will be set up in review.py
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'