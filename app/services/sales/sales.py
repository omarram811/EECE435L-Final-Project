"""
Module: sales.py
Description: Handles sales-related operations and API endpoints.

Endpoints:
    - GET /sales/goods: Retrieves a list of all available goods with their prices.
    - GET /sales/goods/<int:item_id>: Fetches detailed information about a specific item.
    - POST /sales/sale: Processes a new sale, updates the inventory, and records the transaction.

Dependencies:
    - Flask: For creating API endpoints.
    - SQLAlchemy: For database interactions.
"""

from flask import Flask, Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from database.models import Base, InventoryItem, Customer, Sale

# Database setup
DATABASE_URL = "sqlite:///ecommerce.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Blueprint setup
sales_bp = Blueprint("sales", __name__)

# API to display available goods
@sales_bp.route("/goods", methods=["GET"])
def display_goods():
    """
    Retrieves a list of all available goods with their names and prices.
    
    Returns:
        - 200: JSON list of available goods with fields:
            - Name: Name of the product.
            - Price: Price per item.
        - 500: JSON error message if an exception occurs.
    """
    session = Session()
    try:
        goods = session.query(InventoryItem).all()
        available_goods = [{"Name": good.Name, "Price": good.PricePerItem} for good in goods if good.StockCount > 0]
        return jsonify(available_goods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# API to get goods details
@sales_bp.route("/goods/<int:item_id>", methods=["GET"])
def get_goods_details(item_id):
    """
    Retrieves detailed information about a specific item.
    
    Args:
        item_id (int): The ID of the item to retrieve details for.
    
    Returns:
        - 200: JSON object with item details:
            - Name: Name of the product.
            - Category: Category of the product.
            - Price: Price per item.
            - Description: Description of the product.
            - StockCount: Quantity in stock.
            - CreatedAt: ISO format timestamp of item creation.
        - 404: JSON error message if the item is not found.
        - 500: JSON error message if an exception occurs.
    """
    session = Session()
    try:
        item = session.query(InventoryItem).filter_by(ItemID=item_id).first()
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify({
            "Name": item.Name,
            "Category": item.Category,
            "Price": item.PricePerItem,
            "Description": item.Description,
            "StockCount": item.StockCount,
            "CreatedAt": item.CreatedAt.isoformat()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# API to handle a sale
@sales_bp.route("/sale", methods=["POST"])
def create_sale():
    """
    Processes a sale by validating the customer's wallet, item stock, and updating the database.
    
    Request JSON:
        - CustomerUsername (str): The username of the customer making the purchase.
        - ItemName (str): The name of the item to purchase.
        - Quantity (int): The quantity of the item to purchase.
    
    Returns:
        - 201: JSON success message if the sale is completed.
        - 400: JSON error message for:
            - Missing required fields.
            - Insufficient stock.
            - Insufficient wallet balance.
        - 404: JSON error message for:
            - Customer not found.
            - Item not found.
        - 500: JSON error message if an exception occurs.
    """
    data = request.get_json()
    customer_username = data.get("CustomerUsername")
    item_name = data.get("ItemName")
    quantity = data.get("Quantity")

    if not customer_username or not item_name or not quantity:
        return jsonify({"error": "Missing required fields"}), 400

    session = Session()
    try:
        customer = session.query(Customer).filter_by(Username=customer_username).first()
        item = session.query(InventoryItem).filter_by(Name=item_name).first()

        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        if not item:
            return jsonify({"error": "Item not found"}), 404
        if item.StockCount < quantity:
            return jsonify({"error": "Insufficient stock"}), 400
        total_price = item.PricePerItem * quantity
        if customer.WalletBalance < total_price:
            return jsonify({"error": "Insufficient wallet balance"}), 400

        # Update inventory and customer wallet
        item.StockCount -= quantity
        customer.WalletBalance -= total_price

        # Record the sale
        sale = Sale(CustomerID=customer.CustomerID, ItemID=item.ItemID, Quantity=quantity, TotalPrice=total_price)
        session.add(sale)
        session.commit()

        return jsonify({"message": "Sale completed successfully"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

app = Flask(__name__)
app.register_blueprint(sales_bp, url_prefix="/sales")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)