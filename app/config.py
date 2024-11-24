import os

class Config:
    """
    Base configuration class.
    """
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ecommerce.db")  # Default to SQLite

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")  # Replace with a strong key
    TOKEN_EXPIRATION_MINUTES = int(os.getenv("TOKEN_EXPIRATION_MINUTES", 60))  # Token expiry in minutes

    # Flask settings
    DEBUG = bool(int(os.getenv("FLASK_DEBUG", 1)))  # Debug mode on by default

class DevelopmentConfig(Config):
    """
    Development-specific configuration.
    """
    ENV = "development"
    DEBUG = True

class ProductionConfig(Config):
    """
    Production-specific configuration.
    """
    ENV = "production"
    DEBUG = False

# Config dictionary for different environments
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_config(env=None):
    """
    Get the configuration object based on the environment.

    :param env: The environment name (default: use FLASK_ENV environment variable)
    :return: Configuration class
    """
    env = env or os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
