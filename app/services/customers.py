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

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from database.models import Customer, engine

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
