"""
reviews.py

This module defines the Reviews service APIs for managing product reviews. The service
handles creating, updating, deleting, retrieving, and moderating reviews. It interacts
with the database models to manage review-related data.

Blueprint:
    - reviews_bp: Defines the Flask blueprint for the Reviews service.

Endpoints:
    - POST /submit:
        Submit a new review for a product.
    - PUT /update/<int:review_id>:
        Update an existing review.
    - DELETE /delete/<int:review_id>:
        Delete an existing review.
    - GET /product/<int:product_id>:
        Retrieve all reviews for a specific product.
    - GET /customer/<int:customer_id>:
        Retrieve all reviews submitted by a specific customer.
    - PATCH /moderate/<int:review_id>:
        Update moderation status of a review (e.g., flagging inappropriate content).
    - GET /details/<int:review_id>:
        Retrieve detailed information about a specific review.

Dependencies:
    - Flask: Used to define API routes and handle requests.
    - SQLAlchemy: Used to interact with the database models for reviews, customers, and inventory items.
    - app.database.models: Contains the database models and session management.

"""

from flask import Blueprint, request, jsonify
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from database.models import Session, Review, Customer, InventoryItem
#from app.database.models import Session, Review, Customer, InventoryItem

# Define the Flask blueprint for the Reviews service
reviews_bp = Blueprint("reviews", __name__)

# Submit Review
@reviews_bp.route("/submit", methods=["POST"])
def submit_review():
    """
    Submit a new review for a product.

    Request JSON:
        - CustomerID (int): ID of the customer submitting the review.
        - ItemID (int): ID of the product being reviewed.
        - Rating (int): Rating given to the product (e.g., 1-5 stars).
        - Comment (str, optional): Additional feedback or comments about the product.

    Returns:
        JSON response with a success message and the newly created ReviewID.
    """
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
    """
    Update an existing review.

    Path Parameters:
        - review_id (int): ID of the review to be updated.

    Request JSON:
        - Rating (int, optional): Updated rating.
        - Comment (str, optional): Updated comment.

    Returns:
        JSON response indicating success or a 404 error if the review does not exist.
    """
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
    """
    Delete an existing review.

    Path Parameters:
        - review_id (int): ID of the review to be deleted.

    Returns:
        JSON response indicating success or a 404 error if the review does not exist.
    """
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
    """
    Retrieve all reviews for a specific product.

    Path Parameters:
        - product_id (int): ID of the product.

    Returns:
        JSON response with a list of reviews for the product.
    """
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
    """
    Retrieve all reviews submitted by a specific customer.

    Path Parameters:
        - customer_id (int): ID of the customer.

    Returns:
        JSON response with a list of reviews submitted by the customer.
    """
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
    """
    Update the moderation status of a review.

    Path Parameters:
        - review_id (int): ID of the review to be moderated.

    Request JSON:
        - IsFlagged (bool): Moderation status (e.g., flagged or unflagged).

    Returns:
        JSON response with a success message and updated moderation status.
    """
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
    """
    Retrieve detailed information about a specific review.

    Path Parameters:
        - review_id (int): ID of the review.

    Returns:
        JSON response with detailed review information, including:
            - ReviewID
            - CustomerName
            - ProductName
            - Rating
            - Comment
            - CreatedAt
            - IsFlagged
    """
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
