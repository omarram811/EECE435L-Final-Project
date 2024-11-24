"""
create_database.py
==================

This module contains the `create_database` function for setting up the SQLite database and tables for the e-commerce platform.

Functions:
----------
- `create_database()`: Connects to the SQLite database and creates the necessary tables if they don't already exist.
"""

import sqlite3

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

    Execution:
    ----------
    - Establishes a connection to the SQLite database file (creates it if it doesn't exist).
    - Creates the `Customers`, `Inventory`, `Sales`, and `Reviews` tables if they do not already exist.
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

    # Commit changes and close connection
    connection.commit()
    connection.close()
    print("Database and tables created successfully!")

if __name__ == "__main__":
    create_database()
