"""
create_database.py
==================

This module contains the `create_database` function for setting up the SQLite database and tables for the e-commerce platform.

Functions:
----------
- `create_database()`: Connects to the SQLite database and creates the necessary tables if they don't already exist.
"""

import sqlite3
from datetime import datetime

def create_database():
    """
    Creates the SQLite database and necessary tables for the e-commerce platform.

    Tables Created:
    ---------------
    - `Customers`: Stores customer details.
        Fields:
        - CustomerID: Primary key, auto-increment.
        - FullName: Text, required.
        - Username: Text, unique, required.
        - PasswordHash: Text, required.
        - Age: Integer, required, must be greater than 0.
        - Address: Text, required.
        - Gender: Text, required, one of 'Male', 'Female', 'Other'.
        - MaritalStatus: Text, one of 'Single', 'Married', 'Divorced', 'Widowed'.
        - WalletBalance: Real, defaults to 0.0.
        - CreatedAt: Timestamp, defaults to the current timestamp.

    - `Inventory`: Stores inventory items.
        Fields:
        - ItemID: Primary key, auto-increment.
        - Name: Text, required.
        - Category: Text, required, one of 'Food', 'Clothes', 'Accessories', 'Electronics'.
        - PricePerItem: Real, required.
        - Description: Text, optional.
        - StockCount: Integer, required, must be 0 or greater.
        - CreatedAt: Timestamp, defaults to the current timestamp.

    - `Sales`: Tracks sales transactions.
        Fields:
        - SaleID: Primary key, auto-increment.
        - CustomerID: Integer, foreign key referencing Customers.CustomerID.
        - ItemID: Integer, foreign key referencing Inventory.ItemID.
        - Quantity: Integer, required, must be greater than 0.
        - TotalPrice: Real, required.
        - SaleDate: Timestamp, defaults to the current timestamp.

    - `Reviews`: Stores customer reviews for items.
        Fields:
        - ReviewID: Primary key, auto-increment.
        - CustomerID: Integer, foreign key referencing Customers.CustomerID.
        - ItemID: Integer, foreign key referencing Inventory.ItemID.
        - Rating: Integer, required, between 1 and 5 inclusive.
        - Comment: Text, optional.
        - IsFlagged: Boolean, defaults to False.
        - CreatedAt: Timestamp, defaults to the current timestamp.

    - `Wishlist`: Stores wishlist items for customers.
        Fields:
        - WishlistID: Primary key, auto-increment.
        - CustomerID: Integer, foreign key referencing Customers.CustomerID.
        - InventoryItemID: Integer, foreign key referencing Inventory.ItemID.

    Execution:
    ----------
    - Establishes a connection to the SQLite database file (creates it if it doesn't exist).
    - Creates the `Customers`, `Inventory`, `Sales`, `Reviews`, and `Wishlist` tables if they do not already exist.
    - Inserts sample data into the tables.
    - Commits changes to the database and closes the connection.

    Prints:
    -------
    - A success message if the database and tables are created successfully.

    Example Usage:
    --------------
    >>> if __name__ == "__main__":
    >>>     create_database()
    """
    # Connect to SQLite database (creates a file if it doesn't exist)
    connection = sqlite3.connect("ecommerce.db")
    cursor = connection.cursor()

    # Create Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FullName TEXT NOT NULL,
            Username TEXT UNIQUE NOT NULL,
            PasswordHash TEXT NOT NULL,
            Age INTEGER CHECK (Age > 0),
            Address TEXT NOT NULL,
            Gender TEXT CHECK (Gender IN ('Male', 'Female', 'Other')),
            MaritalStatus TEXT CHECK (MaritalStatus IN ('Single', 'Married', 'Divorced', 'Widowed')),
            WalletBalance REAL DEFAULT 0.0,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Inventory (
            ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Category TEXT CHECK (Category IN ('Food', 'Clothes', 'Accessories', 'Electronics')) NOT NULL,
            PricePerItem REAL NOT NULL,
            Description TEXT,
            StockCount INTEGER CHECK (StockCount >= 0) NOT NULL,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales (
            SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER NOT NULL,
            ItemID INTEGER NOT NULL,
            Quantity INTEGER CHECK (Quantity > 0) NOT NULL,
            TotalPrice REAL NOT NULL,
            SaleDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (ItemID) REFERENCES Inventory(ItemID) ON DELETE CASCADE
        )
    ''')

    # Create Reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reviews (
            ReviewID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER NOT NULL,
            ItemID INTEGER NOT NULL,
            Rating INTEGER CHECK (Rating >= 1 AND Rating <= 5) NOT NULL,
            Comment TEXT,
            IsFlagged BOOLEAN DEFAULT FALSE,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (ItemID) REFERENCES Inventory(ItemID) ON DELETE CASCADE
        )
    ''')

    # Create Wishlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Wishlist (
            WishlistID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER NOT NULL,
            InventoryItemID INTEGER NOT NULL,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (InventoryItemID) REFERENCES Inventory(ItemID) ON DELETE CASCADE
        )
    ''')

    # Insert sample data into Customers table
    try:
        cursor.execute('''
            INSERT INTO Customers (FullName, Username, PasswordHash, Age, Address, Gender, MaritalStatus, WalletBalance)
            VALUES
            ('John Doe', 'johndoe', 'hashedpassword', 30, '123 Main St', 'Male', 'Single', 500.0),
            ('Jane Smith', 'janesmith', 'hashedpassword', 25, '456 Elm St', 'Female', 'Married', 300.0)
        ''')
    except sqlite3.IntegrityError as e:
        print(f"Error inserting data into Customers table: {e}")

    # Insert sample data into Inventory table
    cursor.execute('''
        INSERT INTO Inventory (Name, Category, PricePerItem, Description, StockCount)
        VALUES
        ('Laptop', 'Electronics', 1000.0, 'A high-performance laptop', 10),
        ('T-shirt', 'Clothes', 20.0, 'A comfortable cotton t-shirt', 50)
    ''')

    # Insert sample data into Sales table
    cursor.execute('''
        INSERT INTO Sales (CustomerID, ItemID, Quantity, TotalPrice)
        VALUES
        (1, 1, 1, 1000.0),
        (2, 2, 2, 40.0)
    ''')

    # Insert sample data into Reviews table
    cursor.execute('''
        INSERT INTO Reviews (CustomerID, ItemID, Rating, Comment)
        VALUES
        (1, 1, 5, 'Excellent product!'),
        (2, 2, 4, 'Good quality t-shirt.')
    ''')

    # Insert sample data into Wishlist table
    cursor.execute('''
        INSERT INTO Wishlist (customer_id, inventory_item_id)
        VALUES
        (1, 1),
        (2, 1)
    ''')

    # Commit changes and close connection
    connection.commit()
    connection.close()
    print("Database and tables created successfully with sample data!")

if __name__ == "__main__":
    create_database()
