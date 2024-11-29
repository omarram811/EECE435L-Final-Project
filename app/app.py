"""
Flask application setup and blueprint registration.

This module serves as the entry point for the Flask application, registering all services
and handling basic error handling routes.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
from services.customers.customers import customers_bp
from services.inventory.inventory import inventory_bp
from services.reviews.reviews import reviews_bp
from services.sales.sales import sales_bp
from services.cart.cart import cart_bp
from services.recommendations.recommendations import recommendations_bp
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Define the engine (replace with your actual database URL)
engine = create_engine("sqlite:///ecommerce.db")

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pybreaker
import requests
from flask import Flask, jsonify, request

# Create the Flask app instance
app = Flask(__name__)

# Initialize Limiter for rate limiting
limiter = Limiter(
    key_func=get_remote_address,  # Key function for identifying unique clients
    default_limits=["100 per hour"]  # Default rate limits
)

# Attach the Limiter to the Flask app
limiter.init_app(app)

# Initialize Circuit Breaker
circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

# Example service call wrapped with Circuit Breaker
@circuit_breaker
def call_external_service():
    # Replace with actual service call
    response = requests.get("http://external-service/api")
    response.raise_for_status()
    return response.json()

# Apply rate limiting to blueprint routes
app.register_blueprint(customers_bp, url_prefix="/customers", decorators=[limiter.limit("10 per minute")])
app.register_blueprint(inventory_bp, url_prefix="/inventory", decorators=[limiter.limit("10 per minute")])
app.register_blueprint(reviews_bp, url_prefix="/reviews", decorators=[limiter.limit("10 per minute")])
app.register_blueprint(sales_bp, url_prefix="/sales", decorators=[limiter.limit("10 per minute")])
app.register_blueprint(cart_bp, url_prefix="/cart", decorators=[limiter.limit("10 per minute")])
app.register_blueprint(recommendations_bp, url_prefix="/recommendations", decorators=[limiter.limit("10 per minute")])

# Health check route with rate limiting
@app.route("/")
@limiter.limit("5 per minute")
def health_check():
    return jsonify({"message": "API is running successfully!"}), 200

# Error handling example
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500

# example implementation of user-specific rate limiting
class User:
    def __init__(self, username, is_admin=False):
        self.username = username
        self.is_admin = is_admin

USERS = {
    "admin_token": User(username="admin", is_admin=True),
    "user_token": User(username="user", is_admin=False),
}

def get_current_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return User(username="guest", is_admin=False)
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    user = USERS.get(token)
    if not user:
        return User(username="guest", is_admin=False)
    return user

# Custom rate limits based on admin user role
def get_rate_limit():
    user = get_current_user()
    if user.is_admin:
        return "1000 per day"
    return "200 per day"

from pybreaker import CircuitBreakerError
@app.errorhandler(CircuitBreakerError)
def handle_circuit_breaker_error(e):
    return jsonify({"error": "Service currently unavailable. Please try again later."}), 503

# Function to identify abandoned carts
def identify_abandoned_carts():
    """
    Identifies and processes abandoned carts.
    An abandoned cart is defined as a cart item that hasn't been updated
    for more than 24 hours and hasn't resulted in a sale.
    """
    # Define the threshold for abandonment (e.g., 24 hours)
    abandonment_threshold = datetime.utcnow() - timedelta(hours=24)

    # Open a session
    session = Session()

    try:
        # Query to find abandoned carts
        abandoned_carts = session.query(Cart).filter(
            Cart.added_at < abandonment_threshold
        ).all()

        # Process the results
        for cart in abandoned_carts:
            print(f"Abandoned cart: Cart ID {cart.id}, Customer ID {cart.customer_id}, Item ID {cart.item_id}, Added At {cart.added_at}")

            # Optionally, take action such as sending a reminder email or notification
            # Example: send_email_to_customer(cart.customer_id)
        
    except Exception as e:
        print(f"Error identifying abandoned carts: {e}")
    finally:
        # Close the session
        session.close()

# Schedule the abandoned cart identification task
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(func=identify_abandoned_carts, trigger="cron", hour=0)  # Runs daily at midnight
scheduler.start()

# Ensure scheduler shuts down properly
import atexit
from database.models import Session, Cart
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    # Run the application on localhost with debugging enabled
    app.run(host="0.0.0.0", port=5000, debug=True)
