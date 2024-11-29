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
    Creates the SQLite database and necessary tables for the e-commerce platform
    based on the updated models file.

    Tables Created:
    ---------------
    - `Customers`: Stores customer details.
    - `InventoryItems`: Stores inventory items.
    - `Sales`: Tracks sales transactions.
    - `Reviews`: Stores customer reviews for items.
    - `Wishlist`: Stores wishlist items for customers.
    - `Carts`: Stores shopping cart items for customers.
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
            Gender TEXT CHECK (Gender IN ('Male', 'Female', 'Other')) NOT NULL,
            MaritalStatus TEXT CHECK (MaritalStatus IN ('Single', 'Married', 'Divorced', 'Widowed')) NOT NULL,
            WalletBalance REAL DEFAULT 0.0,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create InventoryItems table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS InventoryItems (
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
            SoldAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (ItemID) REFERENCES InventoryItems(ItemID) ON DELETE CASCADE
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
            IsFlagged BOOLEAN DEFAULT 0,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (ItemID) REFERENCES InventoryItems(ItemID) ON DELETE CASCADE
        )
    ''')

    # Create Wishlist table (junction table for many-to-many relationship)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Wishlist (
            WishlistID INTEGER PRIMARY KEY AUTOINCREMENT,
            customerID INTEGER NOT NULL,
            itemID INTEGER NOT NULL,
            FOREIGN KEY (customerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (itemID) REFERENCES InventoryItems(ItemID) ON DELETE CASCADE
        )
    ''')

    # Create Carts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Carts (
            CustomerID INTEGER NOT NULL,
            ItemID INTEGER NOT NULL,
            Quantity INTEGER CHECK (Quantity > 0) NOT NULL,
            AddedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (CustomerID, ItemID),
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (ItemID) REFERENCES InventoryItems(ItemID) ON DELETE CASCADE
        )
    ''')

    # Insert sample data (adjust as needed)
    try:
        cursor.executemany('''
            INSERT INTO Customers (FullName, Username, PasswordHash, Age, Address, Gender, MaritalStatus, WalletBalance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', [
            ('John Doe', 'johndoe', 'hashedpassword', 30, '123 Main St', 'Male', 'Single', 500.0),
            ('Jane Smith', 'janesmith', 'hashedpassword', 25, '456 Elm St', 'Female', 'Married', 300.0)
        ])

        cursor.executemany('''
            INSERT INTO InventoryItems (Name, Category, PricePerItem, Description, StockCount)
            VALUES (?, ?, ?, ?, ?)
        ''', [
            ('Laptop', 'Electronics', 1000.0, 'A high-performance laptop', 10),
            ('T-shirt', 'Clothes', 20.0, 'A comfortable cotton t-shirt', 50)
        ])

        cursor.executemany('''
            INSERT INTO Sales (CustomerID, ItemID, Quantity, TotalPrice)
            VALUES (?, ?, ?, ?)
        ''', [
            (1, 1, 1, 1000.0),  
            (2, 2, 2, 40.0)     
        ])

        cursor.executemany('''
            INSERT INTO Reviews (CustomerID, ItemID, Rating, Comment)
            VALUES (?, ?, ?, ?)
        ''', [
            (1, 1, 5, 'Amazing product! Highly recommend.'),
            (2, 2, 4, 'Good quality but could be cheaper.')
        ])

        cursor.executemany('''
            INSERT INTO Wishlist (customerID, itemID)
            VALUES (?, ?)
        ''', [
            (1, 1),
            (2, 2)
        ])

        cursor.executemany('''
            INSERT INTO Carts (CustomerID, ItemID, Quantity)
            VALUES (?, ?, ?)
        ''', [
            (1, 1, 1),
            (2, 2, 2)
        ])
    except sqlite3.IntegrityError as e:
        print(f"Error inserting sample data: {e}")

    # Commit and close
    connection.commit()
    connection.close()
    print("Database and tables created successfully with sample data!")

if __name__ == "__main__":
    create_database()