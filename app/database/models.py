from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///ecommerce.db"

# Database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)  # Define the sessionmaker
Base = declarative_base()

# Models
class Customer(Base):
    __tablename__ = "Customers"
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
    __tablename__ = "Inventory"
    ItemID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Category = Column(String, nullable=False)
    PricePerItem = Column(Float, nullable=False)
    Description = Column(String, nullable=True)
    StockCount = Column(Integer, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

class Sale(Base):
    __tablename__ = "Sales"
    SaleID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey("Customers.CustomerID"), nullable=False)
    ItemID = Column(Integer, ForeignKey("Inventory.ItemID"), nullable=False)
    Quantity = Column(Integer, nullable=False)
    TotalPrice = Column(Float, nullable=False)
    SaleDate = Column(DateTime, default=datetime.utcnow)
    Customer = relationship("Customer", backref="sales")
    Item = relationship("InventoryItem", backref="sales")

class Review(Base):
    __tablename__ = "Reviews"
    ReviewID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey("Customers.CustomerID"), nullable=False)
    ItemID = Column(Integer, ForeignKey("Inventory.ItemID"), nullable=False)
    Rating = Column(Integer, nullable=False)
    Comment = Column(String, nullable=True)
    IsFlagged = Column(Integer, default=0)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

# Function to initialize the database
def init_db(engine_url="sqlite:///ecommerce.db"):
    engine = create_engine(engine_url)
    Base.metadata.create_all(engine)
    print("Tables created (if not already existing).")
