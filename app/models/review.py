from datetime import datetime
from app import db
from app.models.user import User  # Import User model

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)  # 1-5 stars
    comment = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    def __repr__(self):
        return f'<Review {self.id} - {self.rating} stars>'

# Now set up the relationships from User -> Review
User.reviews_given = db.relationship('Review', foreign_keys=[Review.reviewer_id], backref='reviewer', lazy='dynamic')
User.reviews_received = db.relationship('Review', foreign_keys=[Review.reviewed_id], backref='reviewed', lazy='dynamic')