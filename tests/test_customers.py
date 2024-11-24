import pytest
from app.app import app
from app.database.models import Base, engine, Session, Customer

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Reset the database schema
        Base.metadata.drop_all(bind=engine)  # Drop all tables
        Base.metadata.create_all(bind=engine)  # Create fresh schema

        # Ensure the session is clean
        session = Session()
        session.query(Customer).delete()  # Clear customers table
        session.commit()
        session.close()

        yield client

TEST_CUSTOMERS = [
    {
        "FullName": "Nisrine Bakri",
        "Username": "nisrine.bakri",
        "PasswordHash": "hashedpassword123",
        "Age": 28,
        "Address": "Beirut, Lebanon",
        "Gender": "Female",
        "MaritalStatus": "Single"
    }
]

def test_register_customer(client):
    response = client.post("/customers/register", json=TEST_CUSTOMERS[0])
    print("Register Response Data:", response.json)  # Debug print
    assert response.status_code == 201
    assert response.json["message"] == "Customer registered successfully!"

# Other tests remain unchanged.


def test_get_all_customers(client):
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.get("/customers/")
    print("All Customers Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_customer(client):
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.get("/customers/nisrine.bakri")
    print("Get Customer Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    assert response.json["FullName"] == "Nisrine Bakri"

def test_update_customer(client):
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.put("/customers/1", json={"Address": "Tripoli, Lebanon"})
    print("Update Customer Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    response = client.get("/customers/nisrine.bakri")
    print("Updated Customer Data:", response.json)  # Debug print
    assert response.json["Address"] == "Tripoli, Lebanon"

def test_delete_customer(client):
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.delete("/customers/1")
    print("Delete Customer Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    response = client.get("/customers/nisrine.bakri")
    assert response.status_code == 404

def test_wallet_operations(client):
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.post("/customers/1/charge", json={"amount": 100.50})
    print("Charge Wallet Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    assert response.json["message"] == "Wallet charged successfully!"
    response = client.post("/customers/1/deduct", json={"amount": 50.25})
    print("Deduct Wallet Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    assert response.json["message"] == "Wallet deducted successfully!"
