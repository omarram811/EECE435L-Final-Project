import sqlite3

def create_database():
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
