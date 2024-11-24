from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from app.database.models import InventoryItem, engine

inventory_bp = Blueprint("inventory", __name__)

# Database session setup
Session = sessionmaker(bind=engine)

@inventory_bp.route("/add", methods=["POST"])
def add_good():
    """Add a new good to the inventory."""
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
    """Get all goods in the inventory."""
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
    """Get details of a specific good."""
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
    """Update details of a specific good."""
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
    """Deduct stock of a specific good."""
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
