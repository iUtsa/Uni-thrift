from flask import Blueprint, render_template, request, current_app
from datetime import datetime
from app.models.product import Product, ProductCategory

main = Blueprint('main', __name__)

@main.route('/')
def index():
    featured_products = Product.query.filter_by(is_available=True).order_by(Product.views.desc()).limit(8).all()
    recent_products = Product.query.filter_by(is_available=True).order_by(Product.created_date.desc()).limit(8).all()
    categories = ProductCategory.query.all()
    
    return render_template('index.html', 
                           title='Student Marketplace',
                           featured_products=featured_products,
                           recent_products=recent_products,
                           categories=categories,
                           current_year=datetime.now().year)

@main.route('/search')
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category', 0, type=int)
    sort_by = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    
    products_query = Product.query.filter_by(is_available=True)
    
    if query:
        products_query = products_query.filter(Product.title.contains(query) | 
                                              Product.description.contains(query))
    
    if category_id:
        products_query = products_query.filter_by(category_id=category_id)
    
    if sort_by == 'newest':
        products_query = products_query.order_by(Product.created_date.desc())
    elif sort_by == 'price_low':
        products_query = products_query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        products_query = products_query.order_by(Product.price.desc())
    elif sort_by == 'popular':
        products_query = products_query.order_by(Product.views.desc())
    
    products = products_query.paginate(page=page, per_page=12)
    categories = ProductCategory.query.all()
    
    return render_template('products/list.html',
                          title='Search Results',
                          products=products,
                          categories=categories,
                          query=query,
                          category_id=category_id,
                          sort_by=sort_by,
                          current_year=datetime.now().year)