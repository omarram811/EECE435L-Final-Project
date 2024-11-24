from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database.models import Base, InventoryItem, Customer, Sale

# Database setup
DATABASE_URL = "sqlite:///ecommerce.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Blueprint setup
sales_bp = Blueprint("sales", __name__)

# API to display available goods
@sales_bp.route("/goods", methods=["GET"])
def display_goods():
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
