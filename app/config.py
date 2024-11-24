"""
Application configuration module.

This module provides configuration classes and utilities for managing
environment-specific settings for the Flask application.
"""

import os

class Config:
    """
    Base configuration class.

    Attributes:
        DATABASE_URL (str): The database connection URL.
        SECRET_KEY (str): The secret key for security purposes.
        TOKEN_EXPIRATION_MINUTES (int): Expiration time for authentication tokens in minutes.
        DEBUG (bool): Debug mode toggle.
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
    Configuration for the development environment.

    Inherits:
        Config: The base configuration class.

    Attributes:
        ENV (str): Set to "development".
        DEBUG (bool): Always True for development.
    """
    ENV = "development"
    DEBUG = True

class ProductionConfig(Config):
    """
    Configuration for the production environment.

    Inherits:
        Config: The base configuration class.

    Attributes:
        ENV (str): Set to "production".
        DEBUG (bool): Always False for production.
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
    Retrieve the appropriate configuration class based on the environment.

    Args:
        env (str, optional): The environment name ("development" or "production").
                             Defaults to the FLASK_ENV environment variable or "development".

    Returns:
        class: The corresponding configuration class.
    """
    env = env or os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
