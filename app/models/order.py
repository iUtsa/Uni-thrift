from datetime import datetime
from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True)
    status = db.Column(db.String(20))  # Pending, Paid, Shipped, Completed, Cancelled
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_amount = db.Column(db.Float)
    
    # Foreign keys
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float)  # Price at the time of purchase
    
    # Foreign keys
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))