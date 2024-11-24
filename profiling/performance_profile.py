import time
from flask import Flask
from app.services.sales import sales_bp
from app.services.reviews import reviews_bp
from app.services.customers import customers_bp
from app.services.inventory import inventory_bp
from app.database.models import Base, InventoryItem, Customer, Review, Sale
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(sales_bp, url_prefix="/sales")
app.register_blueprint(reviews_bp, url_prefix="/reviews")
app.register_blueprint(customers_bp, url_prefix="/customers")
app.register_blueprint(inventory_bp, url_prefix="/inventory")

# Set up database connection
DATABASE_URL = "sqlite:///ecommerce.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def seed_database():
    """
    Seed the database with initial data for profiling.
    Ensures no duplicate data is added.
    """
    session = Session()
    try:
        Base.metadata.create_all(engine)  # Ensure tables exist

        # Check and add a customer
        if not session.query(Customer).filter_by(Username="johndoe").first():
            customer = Customer(
                FullName="John Doe",
                Username="johndoe",
                PasswordHash="hashedpassword",
                Age=30,
                Address="123 Main St",
                Gender="Male",
                MaritalStatus="Single",
                WalletBalance=1000.0,
            )
            session.add(customer)

        # Check and add an inventory item
        if not session.query(InventoryItem).filter_by(Name="Laptop").first():
            item = InventoryItem(
                Name="Laptop",
                Category="Electronics",
                PricePerItem=300.0,
                Description="High-performance laptop",
                StockCount=10,
            )
            session.add(item)

        # Check and add a review
        if not session.query(Review).filter_by(Comment="Excellent product!").first():
            review = Review(
                ItemID=1,
                CustomerID=1,
                Rating=5,
                Comment="Excellent product!",
            )
            session.add(review)

        session.commit()
        print("Database seeding completed successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()


def debug_database_state():
    """
    Prints the current state of the database for debugging.
    """
    session = Session()
    try:
        print("\nCurrent Database State:")
        print("Inventory Items:")
        for item in session.query(InventoryItem).all():
            print(f"ID: {item.ItemID}, Name: {item.Name}, Stock: {item.StockCount}, Price: {item.PricePerItem}")
        print("\nCustomers:")
        for customer in session.query(Customer).all():
            print(f"ID: {customer.CustomerID}, Name: {customer.FullName}, Wallet: {customer.WalletBalance}")
        print("\nReviews:")
        for review in session.query(Review).all():
            print(f"ID: {review.ReviewID}, Comment: {review.Comment}, Rating: {review.Rating}, ItemID: {review.ItemID}, CustomerID: {review.CustomerID}")
    finally:
        session.close()

def debug_customer_service(session):
    """
    Debug the current state of customers in the database.

    Args:
        session (Session): SQLAlchemy session to query the database.
    """
    print("\nDebugging Customers Service:")
    customers = session.query(Customer).all()
    if not customers:
        print("No customers found in the database.")
    else:
        for customer in customers:
            print(
                f"Customer ID: {customer.CustomerID}, Username: {customer.Username}, Wallet: {customer.WalletBalance}"
            )



def profile_service(endpoint_name, endpoint_call, debug_state=False):
    """
    Generic function to profile the performance of a service.

    Args:
        endpoint_name (str): The name of the service being profiled.
        endpoint_call (function): The function to call for profiling.
        debug_state (bool): Whether to display database state after the call.
    """
    with app.test_client() as client:
        start_time = time.perf_counter()
        response = endpoint_call(client)
        end_time = time.perf_counter()
        print(f"{endpoint_name} executed in {end_time - start_time:.6f} seconds")
        print(f"Response: {response.get_json()}")
        if debug_state:
            debug_database_state()


if __name__ == "__main__":
    seed_database()  # Seed data before profiling
    print("Database seeded and prepared. Now profiling services...\n")

    print("Before profiling services:")
    debug_database_state()

    # Debug customers specifically before profiling Customers Service
    with Session() as session:
        debug_customer_service(session)

    print("\nProfiling performance of services:")
    profile_service(
        "Sales Service",
        lambda client: client.post(
            "/sales/sale", json={"CustomerUsername": "johndoe", "ItemName": "Laptop", "Quantity": 1}
        ),
    )
    profile_service(
        "Reviews Service",
        lambda client: client.get("/reviews/details/1"),
    )
    profile_service(
        "Customers Service",
        lambda client: client.get("/customers/johndoe"),  # Use username instead of ID
    )
    profile_service(
        "Inventory Service",
        lambda client: client.get("/inventory/goods"),
    )

    print("\nAfter profiling services:")
    debug_database_state()

    # Debug customers specifically after profiling Customers Service
    with Session() as session:
        debug_customer_service(session)
