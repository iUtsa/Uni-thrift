from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Load config
    from app.config import Config
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Set up login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.product import product
    from app.routes.order import order
    from app.routes.api import api
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(product)
    app.register_blueprint(order)
    app.register_blueprint(api)
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        from app.models.user import User
        from app.models.product import Product
        from app.models.order import Order
        return {'db': db, 'User': User, 'Product': Product, 'Order': Order}
    
    return app