from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import sys
from collections import defaultdict

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from database.models import Sale, InventoryItem, Customer, engine

recommendations_bp = Blueprint("recommendations", __name__)

Session = sessionmaker(bind=engine)

@recommendations_bp.route("/recommend/<int:customer_id>", methods=["GET"])
def recommend_products(customer_id):
    """
    Recommend products to a customer based on purchase history.
    
    Args:
        customer_id (int): ID of the customer.
    
    Returns:
        JSON list of recommended products.
    """
    session = Session()
    try:
        # Get items purchased by the customer
        purchased_items = session.query(Sale.ItemID).filter_by(CustomerID=customer_id).all()
        purchased_item_ids = set(item.ItemID for item in purchased_items)
        
        # Simple collaborative filtering: recommend items frequently bought with purchased items
        co_purchase = defaultdict(int)
        sales = session.query(Sale).all()
        for sale in sales:
            if sale.ItemID in purchased_item_ids:
                co_purchase[sale.ItemID] += 1
        
        # Sort items by co-purchase count
        recommended_ids = sorted(co_purchase, key=co_purchase.get, reverse=True)
        
        # Exclude already purchased items
        recommended_ids = [item_id for item_id in recommended_ids if item_id not in purchased_item_ids]
        
        # Get product details
        recommendations = session.query(InventoryItem).filter(InventoryItem.ItemID.in_(recommended_ids)).limit(5).all()
        recommended_products = [{"ItemID": item.ItemID, "Name": item.Name, "PricePerItem": item.PricePerItem} for item in recommendations]
        
        return jsonify(recommended_products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()