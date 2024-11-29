"""
Database Models Module.

This module defines the SQLAlchemy ORM models for the e-commerce application. It includes:
- Customer: Represents customers with personal details and wallet balance.
- InventoryItem: Represents products available for purchase.
- Sale: Represents purchase transactions between customers and inventory items.
- Review: Represents customer reviews for inventory items.
- Cart: Represents items added to the shopping cart.

Functions:
    init_db(engine_url): Initializes the database and creates all tables.

Attributes:
    engine (Engine): The SQLAlchemy engine for managing database connections.
    Session (sessionmaker): A session factory for database operations.
    Base (declarative_base): Base class for all ORM models.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Table, UniqueConstraint, Boolean, MetaData
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

DATABASE_URL = "sqlite:///ecommerce.db"

# Database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)  # Define the sessionmaker
Base = declarative_base()
metadata = MetaData()

# Define the wishlist table
class Wishlist(Base):
    __tablename__ = "Wishlist"
    WishlistID = Column(Integer, primary_key=True, autoincrement=True)
    customerID = Column(Integer, ForeignKey('customers.CustomerID'), nullable=False)
    itemID = Column(Integer, ForeignKey('inventory_items.ItemID'), nullable=False)

    customer = relationship("Customer", backref="Wishlist")
    inventory_item = relationship("InventoryItem", backref="Wishlist")
    __table_args__ = (UniqueConstraint('customerID', 'itemID', name='unique_wishlist_entry'),)

class Customer(Base):
    """
    Represents a customer in the e-commerce platform.

    Attributes:
        CustomerID (int): Unique ID for the customer.
        FullName (str): Full name of the customer.
        Username (str): Unique username for the customer.
        PasswordHash (str): Hashed password for the customer.
        Age (int): Age of the customer.
        Address (str): Address of the customer.
        Gender (str): Gender of the customer.
        MaritalStatus (str): Marital status of the customer.
        WalletBalance (float): Wallet balance of the customer.
        CreatedAt (datetime): Timestamp of when the customer was created.
    """
    __tablename__ = "customers"
    __table_args__ = {'extend_existing': True}
    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String, nullable=False)
    Username = Column(String, unique=True, nullable=False)
    PasswordHash = Column(String, nullable=False)
    Age = Column(Integer, nullable=False)
    Address = Column(String, nullable=False)
    Gender = Column(String, nullable=False)
    MaritalStatus = Column(String, nullable=False)
    WalletBalance = Column(Float, default=0.0)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

class InventoryItem(Base):
    """
    Represents an item in the inventory.

    Attributes:
        ItemID (int): Unique ID for the inventory item.
        Name (str): Name of the item.
        Category (str): Category of the item.
        PricePerItem (float): Price per unit of the item.
        Description (str): Description of the item.
        StockCount (int): Number of units in stock.
        CreatedAt (datetime): Timestamp of when the item was added to inventory.
    """
    __tablename__ = "inventory_items"
    ItemID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Category = Column(String, nullable=False)
    PricePerItem = Column(Float, nullable=False)
    Description = Column(String, nullable=True)
    StockCount = Column(Integer, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

class Sale(Base):
    """
    Represents a sales transaction.

    Attributes:
        SaleID (int): Unique ID for the sale.
        CustomerID (int): ID of the customer who made the purchase.
        ItemID (int): ID of the purchased inventory item.
        Quantity (int): Number of units purchased.
        TotalPrice (float): Total price for the sale.
        SaleDate (datetime): Timestamp of the sale.
        Customer (Customer): Relationship to the customer who made the purchase.
        Item (InventoryItem): Relationship to the purchased inventory item.
    """
    __tablename__ = "sales"
    SaleID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey("customers.CustomerID"), nullable=False)
    ItemID = Column(Integer, ForeignKey("inventory_items.ItemID"), nullable=False)
    Quantity = Column(Integer, nullable=False)
    TotalPrice = Column(Float, nullable=False)
    SoldAt = Column(DateTime, default=datetime.utcnow)
    customer = relationship("Customer", backref="sales")
    inventory_item = relationship("InventoryItem", backref="sales")

class Review(Base):
    """
    Represents a review for an inventory item.

    Attributes:
        ReviewID (int): Unique ID for the review.
        CustomerID (int): ID of the customer who submitted the review.
        ItemID (int): ID of the reviewed inventory item.
        Rating (int): Rating given by the customer.
        Comment (str): Review comment.
        IsFlagged (boolean): Flag indicating whether the review is flagged for moderation.
        CreatedAt (datetime): Timestamp of when the review was created.
    """    
    __tablename__ = "reviews"
    ReviewID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey("customers.CustomerID"), nullable=False)
    ItemID = Column(Integer, ForeignKey("inventory_items.ItemID"), nullable=False)
    Rating = Column(Integer, nullable=False)
    Comment = Column(String, nullable=True)
    IsFlagged = Column(Boolean, default=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    customer = relationship("Customer", backref="reviews")
    inventory_item = relationship("InventoryItem", backref="reviews")

class Cart(Base):
    """
    Represents a shopping cart item.
    
    Attributes:
        CartID (int): Unique ID for the cart entry.
        CustomerID (int): ID of the customer.
        ItemID (int): ID of the inventory item.
        Quantity (int): Quantity of the item.
        AddedAt (datetime): Timestamp when the item was added to the cart.
    """
    __tablename__ = "Cart"
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'), primary_key=True)
    ItemID = Column(Integer, ForeignKey('inventory_items.ItemID'), primary_key=True)
    Quantity = Column(Integer, nullable=False)
    AddedAt = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", backref="Cart")
    inventory_item = relationship("InventoryItem", backref="Cart")
    __table_args__ = (UniqueConstraint('CustomerID', 'ItemID', name='unique_cart_entry'),)

# Function to initialize the database
def init_db(engine_url="sqlite:///ecommerce.db"):
    """
    Initializes the database and creates all tables.

    Args:
        engine_url (str): The database URL to connect to. Defaults to SQLite database.
    """    
    engine = create_engine(engine_url)
    Base.metadata.create_all(engine)
    print("Tables created (if not already existing).")