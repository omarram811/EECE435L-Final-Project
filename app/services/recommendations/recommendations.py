from flask import Flask, Blueprint, request, jsonify
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
    from collections import defaultdict
    session = Session()
    try:
        # Get items purchased by the target customer
        purchased_items = session.query(Sale.ItemID).filter_by(CustomerID=customer_id).all()
        purchased_item_ids = set(item.ItemID for item in purchased_items)
        print(f"Purchased Item IDs for Customer {customer_id}: {purchased_item_ids}")
        
        # Track co-purchases
        co_purchase = defaultdict(int)
        
        # Find all other sales
        all_sales = session.query(Sale).all()
        for sale in all_sales:
            # Skip items purchased by the target customer
            if sale.ItemID in purchased_item_ids:
                continue

            # Check if this sale is by a customer who also bought items the target customer bought
            related_sales = session.query(Sale).filter(Sale.CustomerID == sale.CustomerID).all()
            for related_sale in related_sales:
                if related_sale.ItemID in purchased_item_ids:
                    co_purchase[sale.ItemID] += 1
                    break  # Avoid double-counting for the same customer
        
        print(f"Co-purchase counts: {dict(co_purchase)}")

        # Sort by co-purchase frequency and exclude already purchased items
        recommended_ids = sorted(co_purchase, key=co_purchase.get, reverse=True)
        print(f"Recommended Item IDs before exclusion: {recommended_ids}")
        recommended_ids = [item_id for item_id in recommended_ids if item_id not in purchased_item_ids]
        print(f"Recommended Item IDs: {recommended_ids}")
        
        # Fetch recommendations from inventory
        recommendations = session.query(InventoryItem).filter(InventoryItem.ItemID.in_(recommended_ids)).limit(5).all()
        recommended_products = [{"ItemID": item.ItemID, "Name": item.Name, "PricePerItem": item.PricePerItem} for item in recommendations]

        return jsonify(recommended_products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

app = Flask(__name__)
app.register_blueprint(recommendations_bp, url_prefix="/recommendations")

# Run the Flask app on port 5006
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)