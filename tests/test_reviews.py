"""
Test Suite for the Reviews Service
===================================

This module contains test cases for the Reviews service APIs. The tests ensure that the functionalities
of submitting, updating, deleting, retrieving, and moderating reviews work as expected.

Test Data
---------
- `TEST_CUSTOMER`: Test customer details.
- `TEST_ITEM`: Test inventory item details.
- `TEST_REVIEW`: Test review details.
- `UPDATED_REVIEW`: Updated review details for testing the update functionality.

Fixtures
--------
- `setup_and_cleanup()`: Sets up the test database and test data before each test and cleans up after.
- `client()`: Provides a Flask test client for sending API requests.

Test Cases
----------
1. `test_submit_review(client)`: Tests the ability to submit a review.
2. `test_update_review(client)`: Tests the ability to update an existing review.
3. `test_delete_review(client)`: Tests the ability to delete a review.
4. `test_get_product_reviews(client)`: Tests retrieving all reviews for a specific product.
5. `test_get_customer_reviews(client)`: Tests retrieving all reviews submitted by a specific customer.
6. `test_moderate_review(client)`: Tests the moderation functionality for reviews.
7. `test_get_review_details(client)`: Tests retrieving detailed information about a specific review.
"""

import pytest
from app import create_app
from app.database.models import Base, Session, Customer, InventoryItem, Review
from sqlalchemy import create_engine

# Test Data
TEST_CUSTOMER = {
    "FullName": "Jane Doe",
    "Username": "janedoe",
    "PasswordHash": "hashedpassword",
    "Age": 28,
    "Address": "456 Elm St",
    "Gender": "Female",
    "MaritalStatus": "Married",
    "WalletBalance": 300.0,
}

TEST_ITEM = {
    "Name": "Laptop",
    "Category": "Electronics",
    "PricePerItem": 1000.0,
    "Description": "High-end laptop",
    "StockCount": 50,
}

TEST_REVIEW = {
    "CustomerID": 1,
    "ItemID": 1,
    "Rating": 5,
    "Comment": "Excellent product!"
}

UPDATED_REVIEW = {
    "Rating": 4,
    "Comment": "Good product, but has some flaws."
}

@pytest.fixture(scope="function", autouse=True)
def setup_and_cleanup():
    """
    Fixture to set up the test database and test data before each test
    and clean up afterward.

    - Creates the database schema.
    - Adds test customer and inventory item to the database.
    """
    engine = create_engine("sqlite:///ecommerce.db")
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    # Set up test data
    session = Session()
    session.query(Customer).delete()
    session.query(InventoryItem).delete()
    session.query(Review).delete()
    customer = Customer(**TEST_CUSTOMER)
    item = InventoryItem(**TEST_ITEM)
    session.add(customer)
    session.add(item)
    session.commit()
    yield
    # Cleanup after tests
    session.query(Review).delete()
    session.commit()

@pytest.fixture
def client():
    """
    Fixture to provide a Flask test client for sending API requests.

    Returns:
        client: Flask test client.
    """
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_submit_review(client):
    """
    Test case to validate the review submission API.

    - Sends a POST request with review data.
    - Asserts that the response status code is 201.
    - Asserts that the success message is returned.
    """
    response = client.post("/reviews/submit", json=TEST_REVIEW)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Review submitted successfully!"

def test_update_review(client):
    """
    Test case to validate the review update API.

    - Submits a review and updates it.
    - Asserts that the response status code is 200.
    - Asserts that the success message is returned.
    """
    response = client.post("/reviews/submit", json=TEST_REVIEW)
    assert response.status_code == 201
    review_id = 1  # Assuming review ID is 1
    response = client.put(f"/reviews/update/{review_id}", json=UPDATED_REVIEW)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Review updated successfully!"


def test_delete_review(client):
    """
    Test case to validate the review deletion API.

    - Submits a review and deletes it.
    - Asserts that the response status code is 200.
    - Asserts that the success message is returned.
    """
    response = client.post("/reviews/submit", json=TEST_REVIEW)
    assert response.status_code == 201
    review_id = 1  # Assuming review ID is 1
    response = client.delete(f"/reviews/delete/{review_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Review deleted successfully!"


def test_get_product_reviews(client):
    """
    Test case to validate the API for retrieving reviews for a specific product.

    - Submits a review for a product.
    - Asserts that the response status code is 200.
    - Asserts that the correct number of reviews is returned.
    """
    client.post("/reviews/submit", json=TEST_REVIEW)
    response = client.get("/reviews/product/1")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1  # Expect exactly 1 review

def test_get_customer_reviews(client):
    """
    Test case to validate the API for retrieving reviews submitted by a customer.

    - Submits a review by a customer.
    - Asserts that the response status code is 200.
    - Asserts that the correct number of reviews is returned.
    """
    client.post("/reviews/submit", json=TEST_REVIEW)
    response = client.get("/reviews/customer/1")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1  # Expect exactly 1 review

def test_moderate_review(client):
    """
    Test case to validate the review moderation API.

    - Submits a review and moderates it.
    - Asserts that the response status code is 200.
    - Asserts that the moderation flag is updated correctly.
    """
    client.post("/reviews/submit", json=TEST_REVIEW)
    response = client.patch("/reviews/moderate/1", json={"IsFlagged": 1})
    assert response.status_code == 200
    data = response.get_json()
    assert data["IsFlagged"] == 1

def test_get_review_details(client):
    """
    Test case to validate the API for retrieving detailed information about a review.

    - Submits a review.
    - Asserts that the response status code is 200.
    - Asserts that the correct review details are returned.
    """
    client.post("/reviews/submit", json=TEST_REVIEW)
    response = client.get("/reviews/details/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ReviewID"] == 1
    assert data["CustomerName"] == TEST_CUSTOMER["FullName"]
    assert data["ProductName"] == TEST_ITEM["Name"]
    assert data["Rating"] == TEST_REVIEW["Rating"]
