"""
Validation Module
-----------------
This module provides utilities for validating user input fields,
including usernames, passwords, email addresses, and other attributes.

Functions:
----------
- validate_username(username: str) -> bool
    Validates the username according to specified rules.
- validate_password(password: str) -> bool
    Validates the password to ensure it meets security requirements.
- validate_email(email: str) -> bool
    Validates the format of an email address.
- validate_age(age: int) -> bool
    Validates the age to ensure it's a positive integer.
- validate_gender(gender: str) -> bool
    Validates the gender field against allowed values.
- validate_marital_status(status: str) -> bool
    Validates the marital status field against allowed values.
- validate_positive_float(value: float) -> bool
    Ensures the value is a positive float.
- validate_positive_int(value: int) -> bool
    Ensures the value is a positive integer.
"""

import re

def validate_username(username):
    """
    Validates the username according to specified rules.

    Parameters:
    ----------
    username : str
        The username to validate.

    Returns:
    -------
    bool
        True if valid, False otherwise.
    """
    if not username or len(username) < 3 or len(username) > 30 or " " in username:
        return False
    return True

def validate_password(password):
    """
    Validates the password to ensure it meets security requirements.

    Parameters:
    ----------
    password : str
        The password to validate.

    Returns:
    -------
    bool
        True if valid, False otherwise.
    """
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))

def validate_email(email):
    """
    Validates the format of an email address.

    Parameters:
    ----------
    email : str
        The email address to validate.

    Returns:
    -------
    bool
        True if valid, False otherwise.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def validate_age(age):
    """
    Validates the age to ensure it's a positive integer.

    Parameters:
    ----------
    age : int
        The age to validate.

    Returns:
    -------
    bool
        True if valid, False otherwise.
    """
    return isinstance(age, int) and age > 0

def validate_gender(gender):
    """
    Validates the gender field against allowed values.

    Parameters:
    ----------
    gender : str
        The gender to validate.

    Returns:
    -------
    bool
        True if valid, False otherwise.
    """
    return gender in ["Male", "Female", "Other"]

def validate_marital_status(status):
    """
    Validates the marital status field against allowed values.

    Parameters:
    ----------
    status : str
        The marital status to validate.

    Returns:
    -------
    bool
        True if valid, False otherwise.
    """
    return status in ["Single", "Married", "Divorced", "Widowed"]

def validate_positive_float(value):
    """
    Ensures the value is a positive float.

    Parameters:
    ----------
    value : float
        The value to validate.

    Returns:
    -------
    bool
        True if valid, False otherwise.
    """
    return isinstance(value, float) and value > 0

def validate_positive_int(value):
    """
    Ensures the value is a positive integer.

    Parameters:
    ----------
    value : int
        The value to validate.

    Returns:
    -------
    bool
        True if valid, False otherwise.
    """
    return isinstance(value, int) and value > 0
