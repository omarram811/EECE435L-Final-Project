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
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_submit_review(client):
    response = client.post("/reviews/submit", json=TEST_REVIEW)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Review submitted successfully!"

def test_update_review(client):
    response = client.post("/reviews/submit", json=TEST_REVIEW)
    assert response.status_code == 201
    review_id = 1  # Assuming review ID is 1
    response = client.put(f"/reviews/update/{review_id}", json=UPDATED_REVIEW)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Review updated successfully!"


def test_delete_review(client):
    response = client.post("/reviews/submit", json=TEST_REVIEW)
    assert response.status_code == 201
    review_id = 1  # Assuming review ID is 1
    response = client.delete(f"/reviews/delete/{review_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Review deleted successfully!"


def test_get_product_reviews(client):
    client.post("/reviews/submit", json=TEST_REVIEW)
    response = client.get("/reviews/product/1")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1  # Expect exactly 1 review

def test_get_customer_reviews(client):
    client.post("/reviews/submit", json=TEST_REVIEW)
    response = client.get("/reviews/customer/1")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1  # Expect exactly 1 review

def test_moderate_review(client):
    client.post("/reviews/submit", json=TEST_REVIEW)
    response = client.patch("/reviews/moderate/1", json={"IsFlagged": 1})
    assert response.status_code == 200
    data = response.get_json()
    assert data["IsFlagged"] == 1

def test_get_review_details(client):
    client.post("/reviews/submit", json=TEST_REVIEW)
    response = client.get("/reviews/details/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ReviewID"] == 1
    assert data["CustomerName"] == TEST_CUSTOMER["FullName"]
    assert data["ProductName"] == TEST_ITEM["Name"]
    assert data["Rating"] == TEST_REVIEW["Rating"]
