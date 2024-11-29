"""
Test Suite for Inventory Service APIs
======================================

This module contains unit tests for the Inventory Service APIs. Each test ensures that the
Inventory Service functions as intended, including adding, updating, fetching, and deducting
goods in the inventory.

Dependencies:
    - pytest: For running the test cases.
    - app: The Flask application containing the Inventory Service.
    - models: Database models including `InventoryItem`.

Fixtures:
    - session_cleanup: Ensures the database is cleaned and recreated before each test.
    - client: Provides a test client for making API calls.

Constants:
    - TEST_ITEMS: Sample inventory items for testing.

Functions:
    - test_add_good(client): Tests adding a new good to the inventory.
    - test_get_all_goods(client): Tests retrieving all goods from the inventory.
    - test_get_good(client): Tests retrieving a specific good from the inventory.
    - test_update_good(client): Tests updating the details of a good.
    - test_deduct_good(client): Tests deducting stock from a good in the inventory.
"""

import pytest
from app.app import app
from app.database.models import Base, engine, Session, InventoryItem

@pytest.fixture(autouse=True)
def session_cleanup():
    """
    Fixture to clean up the database before each test.

    Drops and recreates all database tables to ensure tests start with a clean slate.
    """
    # Ensure the database is cleared before every test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.

    Configures the app for testing and yields a test client.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Sample test items for inventory operations
TEST_ITEMS = [
    {
        "Name": "MacBook Pro 16\"",
        "Category": "Electronics",
        "PricePerItem": 2499.99,
        "Description": "High-performance laptop with M1 Max chip.",
        "StockCount": 10  # Ensure enough stock for deduction
    },
    {
        "Name": "Rolex Submariner",
        "Category": "Accessories",
        "PricePerItem": 10999.99,
        "Description": "Luxury diving watch with automatic movement.",
        "StockCount": 5
    }
]

def print_inventory_state():
    """
    Utility function to print the current state of the inventory.

    Queries all goods in the inventory and prints their details. Used for debugging.
    """
    session = Session()
    goods = session.query(InventoryItem).all()
    print("Current Inventory:")
    for good in goods:
        print(f"ItemID: {good.ItemID}, Name: {good.Name}, StockCount: {good.StockCount}")
    session.close()


def test_add_good(client):
    """
    Test Case: Add a new good to the inventory.

    Verifies that a new good can be successfully added and that the appropriate response
    is returned.
    """
    response = client.post("/inventory/add", json=TEST_ITEMS[0])
    print_inventory_state()
    assert response.status_code == 201
    assert response.json["message"] == "Good added to inventory successfully!"

def test_get_good(client):
    """
    Test Case: Retrieve a specific good by ID.

    Verifies that the correct good details are returned for a given ID.
    """
    client.post("/inventory/add", json=TEST_ITEMS[0])
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.json["Name"] == "MacBook Pro 16\""


def test_update_good(client):
    """
    Test Case: Update the details of a specific good.

    Verifies that the price of a good can be updated successfully.
    """
    client.post("/inventory/add", json=TEST_ITEMS[0])
    response = client.put("/inventory/1", json={"PricePerItem": 2399.99})
    assert response.status_code == 200
    response = client.get("/inventory/1")
    assert response.json["PricePerItem"] == 2399.99


def test_deduct_good(client):
    """
    Test Case: Deduct stock from a specific good.

    Verifies that the stock count is reduced correctly after a deduction.
    """
    client.post("/inventory/add", json=TEST_ITEMS[0])
    response = client.get("/inventory/1")  # Fetch stock count
    print("StockCount after adding item:", response.json["StockCount"])  # Debug StockCount
    response = client.post("/inventory/1/deduct", json={"quantity": 2})
    print("Deduct Response JSON:", response.json)  # Debug print
    assert response.status_code == 200
    response = client.get("/inventory/1")
    print("StockCount after deduction:", response.json["StockCount"])  # Debug StockCount
    assert response.json["StockCount"] == 8
