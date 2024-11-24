"""
Unit tests for utility functions in authentication and validation.

This module contains test cases for various utility functions, including token management
(authentication utilities) and validation of user inputs. The tests use pytest to ensure 
correct behavior across multiple scenarios, including parameterized tests for validations.

Tests:
    - Authentication Utilities:
        - Test token generation.
        - Test token verification.
        - Test extracting user ID from token.
    - Validation Utilities:
        - Test username validation.
        - Test password validation.
        - Test email validation.
        - Test age validation.
        - Test gender validation.
        - Test marital status validation.
        - Test positive float validation.
        - Test positive integer validation.
"""

import pytest
from app.utils.authentication import generate_token, verify_token, get_user_id_from_token
from app.utils.validation import (
    validate_username,
    validate_password,
    validate_email,
    validate_age,
    validate_gender,
    validate_marital_status,
    validate_positive_float,
    validate_positive_int
)

MOCK_USER_ID = 123
MOCK_USERNAME = "valid_user123"
MOCK_PASSWORD = "StrongP@ssword1"
MOCK_EMAIL = "user@example.com"
MOCK_AGE = 25
MOCK_GENDER = "Female"
MOCK_MARITAL_STATUS = "Single"
MOCK_FLOAT = 100.50
MOCK_INT = 10
MOCK_TOKEN = None

def test_generate_token():
    """
    Test the generate_token function from authentication utilities.

    Ensures:
        - The generated token is not None.
    """
    global MOCK_TOKEN
    MOCK_TOKEN = generate_token(MOCK_USER_ID)
    assert MOCK_TOKEN is not None

def test_verify_token():
    """
    Test the verify_token function from authentication utilities.

    Ensures:
        - The token payload contains the correct user ID.
    """
    payload = verify_token(MOCK_TOKEN)
    assert payload["user_id"] == MOCK_USER_ID

def test_get_user_id_from_token():
    """
    Test the get_user_id_from_token function from authentication utilities.

    Ensures:
        - The extracted user ID matches the original user ID used to generate the token.
    """
    user_id = get_user_id_from_token(MOCK_TOKEN)
    assert user_id == MOCK_USER_ID

@pytest.mark.parametrize("username,expected", [
    ("valid_user123", True),
    ("invalid user", False),
    ("ab", False),
    ("verylongusernamebeyond30characters", False)
])
def test_validate_username(username, expected):
    """
    Test the validate_username function.

    Parameters:
        - username: Username to validate.
        - expected: Expected boolean result of validation.

    Ensures:
        - Validation results match the expected outcomes for various usernames.
    """
    assert validate_username(username) == expected

@pytest.mark.parametrize("password,expected", [
    ("StrongP@ssword1", True),
    ("weakpassword", False),
    ("Weak1", False),
    ("Password123", False)
])
def test_validate_password(password, expected):
    """
    Test the validate_password function.

    Parameters:
        - password: Password to validate.
        - expected: Expected boolean result of validation.

    Ensures:
        - Validation results match the expected outcomes for various passwords.
    """
    assert validate_password(password) == expected

@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("user.example.com", False),
    ("user@", False),
    ("@example.com", False),
])
def test_validate_email(email, expected):
    """
    Test the validate_email function.

    Parameters:
        - email: Email address to validate.
        - expected: Expected boolean result of validation.

    Ensures:
        - Validation results match the expected outcomes for various email addresses.
    """
    assert validate_email(email) == expected

@pytest.mark.parametrize("age,expected", [
    (25, True),
    (0, False),
    (-5, False),
    ("25", False)
])
def test_validate_age(age, expected):
    """
    Test the validate_age function.

    Parameters:
        - age: Age value to validate.
        - expected: Expected boolean result of validation.

    Ensures:
        - Validation results match the expected outcomes for various age values.
    """
    assert validate_age(age) == expected

@pytest.mark.parametrize("gender,expected", [
    ("Male", True),
    ("Female", True),
    ("Other", True),
    ("Unknown", False),
])
def test_validate_gender(gender, expected):
    """
    Test the validate_gender function.

    Parameters:
        - gender: Gender value to validate.
        - expected: Expected boolean result of validation.

    Ensures:
        - Validation results match the expected outcomes for allowed gender values.
    """
    assert validate_gender(gender) == expected

@pytest.mark.parametrize("status,expected", [
    ("Single", True),
    ("Married", True),
    ("Divorced", True),
    ("Widowed", True),
    ("Complicated", False)
])
def test_validate_marital_status(status, expected):
    """
    Test the validate_marital_status function.

    Parameters:
        - marital_status: Marital status value to validate.
        - expected: Expected boolean result of validation.

    Ensures:
        - Validation results match the expected outcomes for allowed marital status values.
    """
    assert validate_marital_status(status) == expected

@pytest.mark.parametrize("value,expected", [
    (100.50, True),
    (0.0, False),
    (-50.25, False),
    ("100.50", False)
])
def test_validate_positive_float(value, expected):
    """
    Test the validate_positive_float function.

    Parameters:
        - value: Floating-point number to validate.
        - expected: Expected boolean result of validation.

    Ensures:
        - Validation results match the expected outcomes for various floating-point values.
    """
    assert validate_positive_float(value) == expected

@pytest.mark.parametrize("value,expected", [
    (10, True),
    (0, False),
    (-5, False),
    ("10", False)
])
def test_validate_positive_int(value, expected):
    """
    Test the validate_positive_integer function.

    Parameters:
        - value: Integer to validate.
        - expected: Expected boolean result of validation.

    Ensures:
        - Validation results match the expected outcomes for various integer values.
    """
    assert validate_positive_int(value) == expected
