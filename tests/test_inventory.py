import pytest
from app.app import app
from app.database.models import Base, engine, Session, InventoryItem

@pytest.fixture(autouse=True)
def session_cleanup():
    # Ensure the database is cleared before every test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

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
    session = Session()
    goods = session.query(InventoryItem).all()
    print("Current Inventory:")
    for good in goods:
        print(f"ItemID: {good.ItemID}, Name: {good.Name}, StockCount: {good.StockCount}")
    session.close()


def test_add_good(client):
    response = client.post("/inventory/add", json=TEST_ITEMS[0])
    print_inventory_state()
    assert response.status_code == 201
    assert response.json["message"] == "Good added to inventory successfully!"


def test_get_all_goods(client):
    print("BEFORE test_get_all_goods QUERY")
    print_inventory_state()  # Debug before adding items
    for item in TEST_ITEMS:
        client.post("/inventory/add", json=item)
    print_inventory_state()  # Debug after adding items
    response = client.get("/inventory/")
    print("Response JSON:", response.json)  # Debug print
    assert response.status_code == 200
    assert len(response.json) == len(TEST_ITEMS)


def test_get_good(client):
    client.post("/inventory/add", json=TEST_ITEMS[0])
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.json["Name"] == "MacBook Pro 16\""


def test_update_good(client):
    client.post("/inventory/add", json=TEST_ITEMS[0])
    response = client.put("/inventory/1", json={"PricePerItem": 2399.99})
    assert response.status_code == 200
    response = client.get("/inventory/1")
    assert response.json["PricePerItem"] == 2399.99


def test_deduct_good(client):
    client.post("/inventory/add", json=TEST_ITEMS[0])
    response = client.get("/inventory/1")  # Fetch stock count
    print("StockCount after adding item:", response.json["StockCount"])  # Debug StockCount
    response = client.post("/inventory/1/deduct", json={"quantity": 2})
    print("Deduct Response JSON:", response.json)  # Debug print
    assert response.status_code == 200
    response = client.get("/inventory/1")
    print("StockCount after deduction:", response.json["StockCount"])  # Debug StockCount
    assert response.json["StockCount"] == 8
