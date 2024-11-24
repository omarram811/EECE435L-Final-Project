"""
Test Suite for Customer Service
================================

This module contains test cases to validate the functionality of the Customer service APIs.

Fixtures:
---------
- `client`: Configures a Flask test client and resets the database schema before each test.

Constants:
----------
- `TEST_CUSTOMERS`: A list of test customer dictionaries for test cases.

Test Cases:
-----------
- `test_register_customer`: Validates customer registration.
- `test_get_all_customers`: Validates retrieval of all registered customers.
- `test_get_customer`: Validates retrieval of a specific customer's details.
- `test_update_customer`: Validates updating a customer's details.
- `test_delete_customer`: Validates deletion of a customer.
- `test_wallet_operations`: Validates wallet operations (charging and deducting amounts).
"""

import pytest
from app.app import app
from app.database.models import Base, engine, Session, Customer

@pytest.fixture
def client():
    """
    Configures the Flask test client and resets the database schema.

    Yields:
    -------
    - FlaskClient: Configured test client for Flask.
    """
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
    """
    Test Case: Register a new customer.

    Validates:
    ----------
    - Status code: 201 (Created)
    - Response message confirms successful registration.
    """
    response = client.post("/customers/register", json=TEST_CUSTOMERS[0])
    print("Register Response Data:", response.json)  # Debug print
    assert response.status_code == 201
    assert response.json["message"] == "Customer registered successfully!"

# Other tests remain unchanged.


def test_get_all_customers(client):
    """
    Test Case: Retrieve all registered customers.

    Validates:
    ----------
    - Status code: 200 (OK)
    - Number of returned customers matches expected count.
    """
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.get("/customers/")
    print("All Customers Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_customer(client):
    """
    Test Case: Retrieve details of a specific customer.

    Validates:
    ----------
    - Status code: 200 (OK)
    - Customer details in the response match the test data.
    """
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.get("/customers/nisrine.bakri")
    print("Get Customer Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    assert response.json["FullName"] == "Nisrine Bakri"

def test_update_customer(client):
    """
    Test Case: Update a customer's details.

    Validates:
    ----------
    - Status code: 200 (OK)
    - Updated details are reflected in subsequent GET requests.
    """
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.put("/customers/1", json={"Address": "Tripoli, Lebanon"})
    print("Update Customer Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    response = client.get("/customers/nisrine.bakri")
    print("Updated Customer Data:", response.json)  # Debug print
    assert response.json["Address"] == "Tripoli, Lebanon"

def test_delete_customer(client):
    """
    Test Case: Delete a customer.

    Validates:
    ----------
    - Status code: 200 (OK)
    - Customer no longer exists in the database.
    """
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.delete("/customers/1")
    print("Delete Customer Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    response = client.get("/customers/nisrine.bakri")
    assert response.status_code == 404

def test_wallet_operations(client):
    """
    Test Case: Perform wallet operations (charge and deduct amounts).

    Validates:
    ----------
    - Status code: 200 (OK)
    - Wallet balance updates correctly after each operation.
    """
    client.post("/customers/register", json=TEST_CUSTOMERS[0])
    response = client.post("/customers/1/charge", json={"amount": 100.50})
    print("Charge Wallet Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    assert response.json["message"] == "Wallet charged successfully!"
    response = client.post("/customers/1/deduct", json={"amount": 50.25})
    print("Deduct Wallet Response Data:", response.json)  # Debug print
    assert response.status_code == 200
    assert response.json["message"] == "Wallet deducted successfully!"
