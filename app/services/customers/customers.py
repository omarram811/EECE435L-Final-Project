"""
Customers Service Module
-------------------------
This module provides APIs for managing customer information, including registration,
retrieval, updating, deletion, and wallet operations. The routes are defined within
a Flask Blueprint, enabling modular service functionality.

Blueprint:
    customers_bp: Blueprint for the customers service.

Database Session:
    Session: SQLAlchemy session factory for database interactions.

Routes:
    /register (POST): Register a new customer.
    / (GET): Retrieve all customers.
    /<string:username> (GET): Retrieve a specific customer by username.
    /<int:customer_id> (PUT): Update a customer's information.
    /<int:customer_id> (DELETE): Delete a customer.
    /<int:customer_id>/charge (POST): Add funds to a customer's wallet.
    /<int:customer_id>/deduct (POST): Deduct funds from a customer's wallet.
"""
# run: python -m services.customers.customers
from flask import Flask, Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from app.utils.authentication import generate_token, verify_token
from app.utils.validation import validate_username, validate_password
from app.database.models import Customer, InventoryItem, Wishlist, engine, Base
customers_bp = Blueprint("customers", __name__)

# Database session setup
Session = sessionmaker(bind=engine)

@customers_bp.route("/register", methods=["POST"])
def register_customer():
    """
    Register a new customer.

    JSON Parameters:
        FullName (str): Full name of the customer.
        Username (str): Unique username for the customer.
        PasswordHash (str): Hashed password for the customer.
        Age (int): Age of the customer.
        Address (str): Address of the customer.
        Gender (str): Gender of the customer.
        MaritalStatus (str): Marital status of the customer.

    Returns:
        Response: JSON message indicating success or failure.
    """
    data = request.json
    required_fields = ["FullName", "Username", "PasswordHash", "Age", "Address", "Gender", "MaritalStatus"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Validate username and password
    if not validate_username(data["Username"]):
        return jsonify({"error": "Invalid username"}), 400

    if not validate_password(data["PasswordHash"]):
        return jsonify({"error": "Invalid password"}), 400

    session = Session()
    if session.query(Customer).filter_by(Username=data["Username"]).first():
        return jsonify({"error": "Username already taken"}), 400

    customer = Customer(
        FullName=data["FullName"],
        Username=data["Username"],
        PasswordHash=data["PasswordHash"],
        Age=data["Age"],
        Address=data["Address"],
        Gender=data["Gender"],
        MaritalStatus=data["MaritalStatus"],
        WalletBalance=0.0
    )
    session.add(customer)
    session.commit()
    session.close()
    return jsonify({"message": "Customer registered successfully!"}), 201


@customers_bp.route("/login", methods=["POST"])
def login_customer():
    """Authenticate and generate JWT token for the customer."""
    data = request.json
    username = data.get("Username")
    password = data.get("PasswordHash")

    session = Session()
    customer = session.query(Customer).filter_by(Username=username).first()
    
    if not customer or customer.PasswordHash != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(customer.CustomerID)  # Generate JWT token for the customer
    session.close()

    return jsonify({"token": token}), 200

@customers_bp.route("/validate_code", methods=["POST"])
def validate_code_usage():
    """Validate if the customer has permission to use a code."""
    data = request.json
    token = data.get("token")
    code = data.get("code")

    # Validate token
    user_id = verify_token(token)
    if "error" in user_id:
        return jsonify({"error": user_id["error"]}), 401

    # Simulate a list of valid codes for simplicity
    valid_codes = ["CODE123", "CODE456"]

    if code not in valid_codes:
        return jsonify({"error": "Invalid code"}), 400

    return jsonify({"message": "Code is valid"}), 200

# Example of protected route
@customers_bp.route("/protected", methods=["GET"])
def protected_route():
    """A protected route requiring authentication."""
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 401

    user_id = verify_token(token)
    if "error" in user_id:
        return jsonify({"error": user_id["error"]}), 401

    return jsonify({"message": f"Welcome user {user_id['user_id']}"}), 200

@customers_bp.route("/", methods=["GET"])
def get_all_customers():
    """
    Retrieve all customers.

    Returns:
        Response: JSON list of all customer details.
    """
    session = Session()
    customers = session.query(Customer).all()
    session.close()
    return jsonify([
        {
            "CustomerID": c.CustomerID,
            "FullName": c.FullName,
            "Username": c.Username,
            "Age": c.Age,
            "Address": c.Address,
            "Gender": c.Gender,
            "MaritalStatus": c.MaritalStatus,
            "WalletBalance": c.WalletBalance
        } for c in customers
    ]), 200


@customers_bp.route("/<string:username>", methods=["GET"])
def get_customer(username):
    """
    Retrieve a customer by username.

    URL Parameters:
        username (str): Username of the customer.

    Returns:
        Response: JSON object with customer details or error message.
    """
    session = Session()
    customer = session.query(Customer).filter_by(Username=username).first()
    session.close()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({
        "CustomerID": customer.CustomerID,
        "FullName": customer.FullName,
        "Username": customer.Username,
        "Age": customer.Age,
        "Address": customer.Address,
        "Gender": customer.Gender,
        "MaritalStatus": customer.MaritalStatus,
        "WalletBalance": customer.WalletBalance
    }), 200


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """
    Update customer information.

    URL Parameters:
        customer_id (int): Unique ID of the customer.

    JSON Parameters:
        Any valid customer field: Updated values for the specified fields.

    Returns:
        Response: JSON message indicating success or failure.
    """
    data = request.json
    session = Session()
    customer = session.query(Customer).filter_by(CustomerID=customer_id).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    session.commit()
    session.close()
    return jsonify({"message": "Customer information updated successfully!"}), 200


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """
    Delete a customer.

    URL Parameters:
        customer_id (int): Unique ID of the customer.

    Returns:
        Response: JSON message indicating success or failure.
    """
    session = Session()
    customer = session.query(Customer).filter_by(CustomerID=customer_id).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    session.delete(customer)
    session.commit()
    session.close()
    return jsonify({"message": "Customer deleted successfully!"}), 200


@customers_bp.route("/<int:customer_id>/charge", methods=["POST"])
def charge_wallet(customer_id):
    """
    Charge a customer's wallet.

    URL Parameters:
        customer_id (int): Unique ID of the customer.

    JSON Parameters:
        amount (float): Amount to add to the wallet.

    Returns:
        Response: JSON message indicating success or failure.
    """
    data = request.json
    amount = data.get("amount")
    if not amount or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    session = Session()
    customer = session.query(Customer).filter_by(CustomerID=customer_id).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    customer.WalletBalance += amount
    session.commit()
    session.close()
    return jsonify({"message": "Wallet charged successfully!"}), 200


@customers_bp.route("/<int:customer_id>/deduct", methods=["POST"])
def deduct_wallet(customer_id):
    """
    Deduct money from a customer's wallet.

    URL Parameters:
        customer_id (int): Unique ID of the customer.

    JSON Parameters:
        amount (float): Amount to deduct from the wallet.

    Returns:
        Response: JSON message indicating success or failure.
    """
    data = request.json
    amount = data.get("amount")
    if not amount or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    session = Session()
    customer = session.query(Customer).filter_by(CustomerID=customer_id).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    if customer.WalletBalance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    customer.WalletBalance -= amount
    session.commit()
    session.close()
    return jsonify({"message": "Wallet deducted successfully!"}), 200

@customers_bp.route("/<int:customer_id>/wishlist", methods=["POST"])
def add_to_wishlist(customer_id):
    """
    Add a product to the customer's wishlist.
    
    JSON Parameters:
        - item_id (int): ID of the product to add.
    
    Returns:
        JSON message indicating success or failure.
    """
    data = request.json
    item_id = data.get("item_id")
    if not item_id:
        return jsonify({"error": "Missing item_id"}), 400

    session = Session()
    try:
        customer = session.query(Customer).filter_by(CustomerID=customer_id).first()
        item = session.query(InventoryItem).filter_by(ItemID=item_id).first()
        if not customer or not item:
            return jsonify({"error": "Customer or Item not found"}), 404

        # Check if already in wishlist
        existing_entry = session.query(Wishlist).filter_by(customerID=customer_id, itemID=item_id).first()
        if existing_entry:
            return jsonify({"error": "Item already in wishlist"}), 400

        wishlist_entry = Wishlist(customerID=customer_id, itemID=item_id)
        session.add(wishlist_entry)
        session.commit()
        return jsonify({"message": "Item added to wishlist"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@customers_bp.route("/<int:customer_id>/wishlist", methods=["GET"])
def view_wishlist(customer_id):
    """
    View the customer's wishlist.

    Returns:
        JSON list of items in the wishlist.
    """
    session = Session()
    try:
        wishlist_entries = session.query(Wishlist).filter_by(customerID=customer_id).all()
        if not wishlist_entries:
            return jsonify([]), 200

        wishlist = [
            {
                "ItemID": entry.itemID,
                "Name": entry.inventory_item.Name,
                "PricePerItem": entry.inventory_item.PricePerItem
            } for entry in wishlist_entries
        ]
        return jsonify(wishlist), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@customers_bp.route("/<int:customer_id>/wishlist/<int:item_id>", methods=["DELETE"])
def remove_from_wishlist(customer_id, item_id):
    """
    Remove a product from the customer's wishlist.
    
    Returns:
        JSON message indicating success or failure.
    """
    session = Session()
    try:
        wishlist_entry = session.query(Wishlist).filter_by(customerID=customer_id, itemID=item_id).first()
        if not wishlist_entry:
            return jsonify({"error": "Item not found in wishlist"}), 404

        session.delete(wishlist_entry)
        session.commit()
        return jsonify({"message": "Item removed from wishlist"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

app = Flask(__name__)
app.register_blueprint(customers_bp, url_prefix="/customers")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)