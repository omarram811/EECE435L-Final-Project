"""
Inventory Service
==================
This module provides API endpoints to manage inventory items. The inventory service
allows adding new goods, retrieving details of specific goods or all goods, updating goods, 
and deducting stock of goods.

Blueprint:
----------
- inventory_bp: Blueprint for the inventory module.

Endpoints:
----------
- POST /add: Add a new good to the inventory.
- GET /: Retrieve all goods in the inventory.
- GET /<int:item_id>: Retrieve details of a specific good.
- PUT /<int:item_id>: Update details of a specific good.
- POST /<int:item_id>/deduct: Deduct stock of a specific good.

Dependencies:
-------------
- Flask
- SQLAlchemy ORM
"""

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from database.models import InventoryItem, engine
#from app.database.models import InventoryItem, engine

inventory_bp = Blueprint("inventory", __name__)

# Database session setup
Session = sessionmaker(bind=engine)

@inventory_bp.route("/add", methods=["POST"])
def add_good():
    """
    Add a new good to the inventory.

    Request JSON Parameters:
    ------------------------
    - Name (str): The name of the good.
    - Category (str): The category of the good.
    - PricePerItem (float): Price per item.
    - Description (str): Description of the good.
    - StockCount (int): Available stock count.

    Returns:
    --------
    - 201: JSON message indicating success.
    - 400: JSON error message if a required field is missing.
    """
    data = request.json
    required_fields = ["Name", "Category", "PricePerItem", "Description", "StockCount"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    session = Session()
    good = InventoryItem(
        Name=data["Name"],
        Category=data["Category"],
        PricePerItem=data["PricePerItem"],
        Description=data["Description"],
        StockCount=data["StockCount"]
    )
    session.add(good)
    session.commit()
    session.close()
    return jsonify({"message": "Good added to inventory successfully!"}), 201


@inventory_bp.route("/", methods=["GET"])
def get_all_goods():
    """
    Get all goods in the inventory.

    Returns:
    --------
    - 200: JSON list of all goods with their details.
    """
    session = Session()
    goods = session.query(InventoryItem).all()
    session.close()
    return jsonify([
        {
            "ItemID": g.ItemID,
            "Name": g.Name,
            "Category": g.Category,
            "PricePerItem": g.PricePerItem,
            "Description": g.Description,
            "StockCount": g.StockCount
        } for g in goods
    ]), 200


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_good(item_id):
    """
    Get details of a specific good.

    Parameters:
    -----------
    - item_id (int): The ID of the good to retrieve.

    Returns:
    --------
    - 200: JSON details of the specified good.
    - 404: JSON error message if the good is not found.
    """
    session = Session()
    good = session.query(InventoryItem).filter_by(ItemID=item_id).first()
    session.close()
    if not good:
        return jsonify({"error": "Good not found"}), 404
    return jsonify({
        "ItemID": good.ItemID,
        "Name": good.Name,
        "Category": good.Category,
        "PricePerItem": good.PricePerItem,
        "Description": good.Description,
        "StockCount": good.StockCount
    }), 200


@inventory_bp.route("/<int:item_id>", methods=["PUT"])
def update_good(item_id):
    """
    Update details of a specific good.

    Parameters:
    -----------
    - item_id (int): The ID of the good to update.
    - JSON body with keys matching the attributes of the good.

    Returns:
    --------
    - 200: JSON message indicating successful update.
    - 404: JSON error message if the good is not found.
    """
    data = request.json
    session = Session()
    good = session.query(InventoryItem).filter_by(ItemID=item_id).first()
    if not good:
        return jsonify({"error": "Good not found"}), 404

    for key, value in data.items():
        if hasattr(good, key):
            setattr(good, key, value)
    session.commit()
    session.close()
    return jsonify({"message": "Good information updated successfully!"}), 200


@inventory_bp.route("/<int:item_id>/deduct", methods=["POST"])
def deduct_good(item_id):
    """
    Deduct stock of a specific good.

    Parameters:
    -----------
    - item_id (int): The ID of the good.
    - quantity (int): The quantity to deduct (in the JSON body).

    Returns:
    --------
    - 200: JSON message indicating successful deduction.
    - 400: JSON error message for invalid quantity or insufficient stock.
    - 404: JSON error message if the good is not found.
    """
    data = request.json
    quantity = data.get("quantity")
    if not quantity or quantity <= 0:
        return jsonify({"error": "Invalid quantity"}), 400

    session = Session()
    good = session.query(InventoryItem).filter_by(ItemID=item_id).first()
    if not good:
        return jsonify({"error": "Good not found"}), 404
    if good.StockCount < quantity:
        return jsonify({"error": "Insufficient stock"}), 400

    good.StockCount -= quantity
    session.commit()
    session.close()
    return jsonify({"message": f"{quantity} items deducted from stock"}), 200
