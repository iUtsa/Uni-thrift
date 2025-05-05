from datetime import datetime
from app import db

class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    condition = db.Column(db.String(50))  # New, Like New, Good, Fair, Poor
    location = db.Column(db.String(120))
    is_available = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    
    # Foreign keys
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    
    # Relationships
    images = db.relationship('ProductImage', backref='product', cascade='all, delete-orphan')
    orders = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def increment_views(self):
        self.views += 1
        db.session.commit()
    
    def __repr__(self):
        return f'<Product {self.title}>'

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120))
    is_primary = db.Column(db.Boolean, default=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))