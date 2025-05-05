from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app import db
from app.models.product import Product, ProductCategory
from app.models.user import User
from app.models.order import Order

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/products')
def get_products():
    """API endpoint to get products with filtering"""
    query = request.args.get('q', '')
    category_id = request.args.get('category', 0, type=int)
    
    products_query = Product.query.filter_by(is_available=True)
    
    if query:
        products_query = products_query.filter(Product.title.contains(query) | 
                                             Product.description.contains(query))
    
    if category_id:
        products_query = products_query.filter_by(category_id=category_id)
    
    products = products_query.order_by(Product.created_date.desc()).limit(20).all()
    
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'title': product.title,
            'price': product.price,
            'image': product.images[0].file_name if product.images else 'default_product.jpg',
            'condition': product.condition,
            'location': product.location,
            'seller': product.seller.username
        })
    
    return jsonify(result)

@api.route('/categories')
def get_categories():
    """API endpoint to get all product categories"""
    categories = ProductCategory.query.all()
    
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name
        })
    
    return jsonify(result)

@api.route('/user/<int:id>/products')
def get_user_products(id):
    """API endpoint to get products from a specific user"""
    user = User.query.get_or_404(id)
    products = Product.query.filter_by(seller_id=id, is_available=True).all()
    
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'title': product.title,
            'price': product.price,
            'image': product.images[0].file_name if product.images else 'default_product.jpg'
        })
    
    return jsonify(result)

@api.route('/product/<int:id>')
def get_product(id):
    """API endpoint to get details of a specific product"""
    product = Product.query.get_or_404(id)
    
    images = []
    for image in product.images:
        images.append(image.file_name)
    
    result = {
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'price': product.price,
        'condition': product.condition,
        'location': product.location,
        'created_date': product.created_date.strftime('%Y-%m-%d'),
        'views': product.views,
        'seller': {
            'id': product.seller.id,
            'username': product.seller.username
        },
        'category': {
            'id': product.category.id,
            'name': product.category.name
        },
        'images': images
    }
    
    return jsonify(result)