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

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pybreaker
import requests
from flask import Flask, jsonify, request

# Create the Flask app instance
app = Flask(__name__)

# Initialize Limiter for rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

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

# Register blueprints for all services
# app.register_blueprint(customers_bp, url_prefix="/customers")
# app.register_blueprint(inventory_bp, url_prefix="/inventory")
# app.register_blueprint(reviews_bp, url_prefix="/reviews")
# app.register_blueprint(sales_bp, url_prefix="/sales")

# Health check route with rate limiting
@app.route("/")
@limiter.limit("5 per minute")
def health_check():
    return jsonify({"message": "API is running successfully!"}), 200

# Health check route
# @app.route("/")
# def health_check():
#     """
#     Health check route to confirm the API is running.

#     Returns:
#         JSON response with success message and HTTP 200 status.
#     """
#     return jsonify({"message": "API is running successfully!"}), 200

# Error handling example
@app.errorhandler(404)
def not_found_error(error):
    """
    Custom error handler for 404 - Resource not found.

    Args:
        error: The error object for the 404 exception.

    Returns:
        JSON response with error message and HTTP 404 status.
    """
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Custom error handler for 500 - Internal server error.

    Args:
        error: The error object for the 500 exception.

    Returns:
        JSON response with error message and HTTP 500 status.
    """
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
    """
    Retrieve the current user based on the Authorization header.

    Returns:
        User object if authenticated, else raises an error.
    """
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

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[get_rate_limit]
)

from pybreaker import CircuitBreakerError
@app.errorhandler(CircuitBreakerError)
def handle_circuit_breaker_error(e):
    return jsonify({"error": "Service currently unavailable. Please try again later."}), 503

if __name__ == "__main__":
    # Run the application on localhost with debugging enabled
    app.run(host="0.0.0.0", port=5000, debug=True)
