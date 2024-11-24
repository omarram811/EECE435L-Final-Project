import pytest
from flask import Flask
from app.services.sales import sales_bp
from app.database.models import Base, Customer, InventoryItem, Sale
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///ecommerce.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(sales_bp, url_prefix="/sales")
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)

            session = Session()

            customer = Customer(
                FullName="John Doe",
                Username="johndoe",
                PasswordHash="hashedpassword",
                Age=30,
                Address="123 Main St",
                Gender="Male",
                MaritalStatus="Single",
                WalletBalance=500.0
            )
            item = InventoryItem(
                Name="Laptop",
                Category="Electronics",
                PricePerItem=300.0,
                Description="High-performance laptop",
                StockCount=10
            )
            session.add(customer)
            session.add(item)
            session.commit()
            session.close()

        yield client

def test_display_goods(client):
    response = client.get("/sales/goods")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["Name"] == "Laptop"
    assert data[0]["Price"] == 300.0

def test_get_goods_details(client):
    response = client.get("/sales/goods/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["Name"] == "Laptop"
    assert data["Category"] == "Electronics"
    assert data["Price"] == 300.0

def test_create_sale(client):
    response = client.post("/sales/sale", json={
        "CustomerUsername": "johndoe",
        "ItemName": "Laptop",
        "Quantity": 1
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Sale completed successfully"

    session = Session()
    customer = session.query(Customer).filter_by(Username="johndoe").first()
    item = session.query(InventoryItem).filter_by(Name="Laptop").first()
    assert customer.WalletBalance == 200.0  # 500 - 300
    assert item.StockCount == 9  # 10 - 1
    session.close()

def test_insufficient_wallet_balance(client):
    response = client.post("/sales/sale", json={
        "CustomerUsername": "johndoe",
        "ItemName": "Laptop",
        "Quantity": 2  # Total price: 600 > Wallet balance: 500
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Insufficient wallet balance"

def test_insufficient_stock(client):
    response = client.post("/sales/sale", json={
        "CustomerUsername": "johndoe",
        "ItemName": "Laptop",
        "Quantity": 20  # Stock: 10
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Insufficient stock"
