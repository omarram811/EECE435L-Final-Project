from memory_profiler import profile
from flask import Flask
from app.services.sales.sales import sales_bp
from app.services.reviews.reviews import reviews_bp
from app.services.customers.customers import customers_bp
from app.services.inventory.inventory import inventory_bp

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(sales_bp, url_prefix="/sales")
app.register_blueprint(reviews_bp, url_prefix="/reviews")
app.register_blueprint(customers_bp, url_prefix="/customers")
app.register_blueprint(inventory_bp, url_prefix="/inventory")


@profile
def profile_sales_service():
    with app.test_client() as client:
        # Simulate a POST request to create a sale
        data = {"CustomerUsername": "johndoe", "ItemName": "Laptop", "Quantity": 1}
        client.post("/sales/sale", json=data)


@profile
def profile_reviews_service():
    with app.test_client() as client:
        # Simulate a GET request to fetch review details
        client.get("/reviews/details/1")


@profile
def profile_customers_service():
    with app.test_client() as client:
        # Simulate a GET request to fetch customer details
        client.get("/customers/1")


@profile
def profile_inventory_service():
    with app.test_client() as client:
        # Simulate a GET request to fetch available goods
        client.get("/inventory/goods")


if __name__ == "__main__":
    profile_sales_service()
    profile_reviews_service()
    profile_customers_service()
    profile_inventory_service()
