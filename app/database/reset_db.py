from models import Base, create_engine  # Adjust based on your project structure

def reset_db(engine_url="sqlite:///ecommerce.db"):
    engine = create_engine(engine_url)
    Base.metadata.drop_all(engine)  # Drop all tables
    Base.metadata.create_all(engine)  # Recreate tables
    print("Database reset successfully.")

if __name__ == "__main__":
    reset_db()  # Run the function