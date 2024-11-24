from flask import Flask
from sqlalchemy import create_engine
from app.database.models import Base

# SQLite Database URL
DATABASE_URL = "sqlite:///ecommerce.db"

# Function to initialize the database with SQLAlchemy
def create_database_with_sqlalchemy(engine_url=DATABASE_URL):
    engine = create_engine(engine_url)
    Base.metadata.create_all(engine)
    print("Tables created (if not already existing).")

# Flask application factory
def create_app(engine_url=DATABASE_URL):
    app = Flask(__name__)

    # Initialize the database
    create_database_with_sqlalchemy(engine_url)

    # Import blueprints for all services
    from app.services.customers import customers_bp
    from app.services.inventory import inventory_bp
    from app.services.sales import sales_bp
    from app.services.reviews import reviews_bp

    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(sales_bp, url_prefix="/sales")
    app.register_blueprint(reviews_bp, url_prefix="/reviews")

    return app
