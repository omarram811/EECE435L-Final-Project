from flask import Flask, Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from database.models import Cart, Customer, InventoryItem, Sale, engine

cart_bp = Blueprint("cart", __name__)

Session = sessionmaker(bind=engine)

@cart_bp.route("/<int:customer_id>/cart", methods=["POST"])
def add_to_cart(customer_id):
    """
    Add an item to the customer's cart.
    
    JSON Parameters:
        - item_id (int): ID of the product to add.
        - quantity (int): Quantity to add.
    
    Returns:
        JSON message indicating success or failure.
    """
    data = request.json
    item_id = data.get("item_id")
    quantity = data.get("quantity")
    if not item_id or not quantity:
        return jsonify({"error": "Missing item_id or quantity"}), 400
    
    session = Session()
    try:
        customer = session.query(Customer).filter_by(CustomerID=customer_id).first()
        item = session.query(InventoryItem).filter_by(ItemID=item_id).first()
        if not customer or not item:
            return jsonify({"error": "Customer or Item not found"}), 404
        cart_item = session.query(Cart).filter_by(CustomerID=customer_id, ItemID=item_id).first()
        if cart_item:
            cart_item.Quantity += quantity
        else:
            cart_item = Cart(CustomerID=customer_id, ItemID=item_id, Quantity=quantity, AddedAt=datetime.utcnow())
            session.add(cart_item)
        session.commit()
        return jsonify({"message": "Item added to cart"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@cart_bp.route("/<int:customer_id>/cart", methods=["GET"])
def view_cart(customer_id):
    """
    View the customer's cart.
    
    Returns:
        JSON list of cart items.
    """
    session = Session()
    try:
        cart_items = session.query(Cart).filter_by(CustomerID=customer_id).all()
        cart = [{
            "ItemID": item.ItemID,
            "Name": item.inventory_item.Name,
            "Quantity": item.Quantity,
            "AddedAt": item.AddedAt.isoformat()
        } for item in cart_items]
        return jsonify(cart), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@cart_bp.route("/<int:customer_id>/cart/<int:item_id>", methods=["DELETE"])
def remove_from_cart(customer_id, item_id):
    """
    Remove an item from the customer's cart.
    
    Returns:
        JSON message indicating success or failure.
    """
    session = Session()
    try:
        cart_item = session.query(Cart).filter_by(CustomerID=customer_id, ItemID=item_id).first()
        if not cart_item:
            return jsonify({"error": "Cart item not found"}), 404
        session.delete(cart_item)
        session.commit()
        return jsonify({"message": "Item removed from cart"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Scheduled task to identify abandoned carts
def identify_abandoned_carts():
    session = Session()
    try:
        threshold = datetime.utcnow() - timedelta(hours=24)  # 24 hours threshold
        abandoned_carts = session.query(Cart).filter(Cart.AddedAt < threshold).all()
        for cart in abandoned_carts:
            customer = session.query(Customer).filter_by(CustomerID=cart.CustomerID).first()
            # Implement notification logic here (e.g., send email)
            print(f"Notify {customer.Username} about abandoned cart.")
            session.delete(cart)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error identifying abandoned carts: {e}")
    finally:
        session.close()
    
app = Flask(__name__)
app.register_blueprint(cart_bp, url_prefix="/cart")

# Run the Flask app on port 5005
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)