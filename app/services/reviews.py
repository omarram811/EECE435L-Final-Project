from flask import Blueprint, request, jsonify
from app.database.models import Session, Review, Customer, InventoryItem

reviews_bp = Blueprint("reviews", __name__)

# Submit Review
@reviews_bp.route("/submit", methods=["POST"])
def submit_review():
    data = request.get_json()
    session = Session()

    review = Review(
        CustomerID=data["CustomerID"],
        ItemID=data["ItemID"],
        Rating=data["Rating"],
        Comment=data.get("Comment", "")
    )
    session.add(review)
    session.commit()

    return jsonify({"message": "Review submitted successfully!", "ReviewID": review.ReviewID}), 201

# Update Review
@reviews_bp.route('/update/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    session = Session()
    review = session.query(Review).get(review_id)
    if not review:
        return jsonify({"message": "Review not found"}), 404

    review.Rating = data.get("Rating", review.Rating)
    review.Comment = data.get("Comment", review.Comment)
    session.commit()
    session.close()
    return jsonify({"message": "Review updated successfully!"}), 200


# Delete Review
@reviews_bp.route('/delete/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    session = Session()
    review = session.query(Review).get(review_id)
    if not review:
        return jsonify({"message": "Review not found"}), 404

    session.delete(review)
    session.commit()
    session.close()
    return jsonify({"message": "Review deleted successfully!"}), 200


# Get Product Reviews
@reviews_bp.route("/product/<int:product_id>", methods=["GET"])
def get_product_reviews(product_id):
    session = Session()

    reviews = session.query(Review).filter_by(ItemID=product_id).all()
    return jsonify([{
        "ReviewID": review.ReviewID,
        "CustomerID": review.CustomerID,
        "Rating": review.Rating,
        "Comment": review.Comment,
        "CreatedAt": review.CreatedAt,
        "IsFlagged": review.IsFlagged
    } for review in reviews])

# Get Customer Reviews
@reviews_bp.route("/customer/<int:customer_id>", methods=["GET"])
def get_customer_reviews(customer_id):
    session = Session()

    reviews = session.query(Review).filter_by(CustomerID=customer_id).all()
    return jsonify([{
        "ReviewID": review.ReviewID,
        "ItemID": review.ItemID,
        "Rating": review.Rating,
        "Comment": review.Comment,
        "CreatedAt": review.CreatedAt,
        "IsFlagged": review.IsFlagged
    } for review in reviews])

# Moderate Review
@reviews_bp.route("/moderate/<int:review_id>", methods=["PATCH"])
def moderate_review(review_id):
    data = request.get_json()
    session = Session()

    review = session.query(Review).get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    review.IsFlagged = data["IsFlagged"]
    session.commit()

    return jsonify({"message": "Review moderation updated successfully!", "IsFlagged": review.IsFlagged})

# Get Review Details
@reviews_bp.route("/details/<int:review_id>", methods=["GET"])
def get_review_details(review_id):
    session = Session()

    review = session.query(Review).get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    customer = session.query(Customer).get(review.CustomerID)
    product = session.query(InventoryItem).get(review.ItemID)

    return jsonify({
        "ReviewID": review.ReviewID,
        "CustomerName": customer.FullName,
        "ProductName": product.Name,
        "Rating": review.Rating,
        "Comment": review.Comment,
        "CreatedAt": review.CreatedAt,
        "IsFlagged": review.IsFlagged
    })
