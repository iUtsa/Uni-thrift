from app import create_app, db
from app.models.user import User
from app.models.product import ProductCategory, Product
from app.models.order import Order
from app.models.review import Review

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    
    # Create initial categories if none exist
    if ProductCategory.query.count() == 0:
        categories = [
            ProductCategory(name="Textbooks", description="Academic books and course materials"),
            ProductCategory(name="Electronics", description="Laptops, phones, and other devices"),
            ProductCategory(name="Furniture", description="Desks, chairs, and dorm room items"),
            ProductCategory(name="Clothing", description="Apparel and accessories"),
            ProductCategory(name="Services", description="Tutoring, rides, and other services"),
            ProductCategory(name="Other", description="Miscellaneous items")
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        print("Database initialized with categories.")
    else:
        print("Database already contains categories.")