from flask import Flask, jsonify
from app.services.customers import customers_bp
from app.services.inventory import inventory_bp
from app.services.reviews import reviews_bp
from app.services.sales import sales_bp

# Create Flask app
app = Flask(__name__)

# Register blueprints for all services
app.register_blueprint(customers_bp, url_prefix="/customers")
app.register_blueprint(inventory_bp, url_prefix="/inventory")
app.register_blueprint(reviews_bp, url_prefix="/reviews")
app.register_blueprint(sales_bp, url_prefix="/sales")

# Health check route
@app.route("/")
def health_check():
    return jsonify({"message": "API is running successfully!"}), 200

# Error handling example
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Run the application on localhost with debugging enabled
    app.run(host="0.0.0.0", port=5000, debug=True)
