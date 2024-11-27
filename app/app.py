"""
Flask application setup and blueprint registration.

This module serves as the entry point for the Flask application, registering all services
and handling basic error handling routes.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
from app.services.customers.customers import customers_bp
from services.inventory import inventory_bp
from services.reviews import reviews_bp
from services.sales import sales_bp

from flask import Flask, jsonify
# from app.services.customers import customers_bp
# from app.services.inventory import inventory_bp
# from app.services.reviews import reviews_bp
# from app.services.sales import sales_bp

# Create the Flask app instance
app = Flask(__name__)

# Register blueprints for all services
app.register_blueprint(customers_bp, url_prefix="/customers")
app.register_blueprint(inventory_bp, url_prefix="/inventory")
app.register_blueprint(reviews_bp, url_prefix="/reviews")
app.register_blueprint(sales_bp, url_prefix="/sales")

# Health check route
@app.route("/")
def health_check():
    """
    Health check route to confirm the API is running.

    Returns:
        JSON response with success message and HTTP 200 status.
    """
    return jsonify({"message": "API is running successfully!"}), 200

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

if __name__ == "__main__":
    # Run the application on localhost with debugging enabled
    app.run(host="0.0.0.0", port=5000, debug=True)
