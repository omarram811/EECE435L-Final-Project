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
    global MOCK_TOKEN
    MOCK_TOKEN = generate_token(MOCK_USER_ID)
    assert MOCK_TOKEN is not None

def test_verify_token():
    payload = verify_token(MOCK_TOKEN)
    assert payload["user_id"] == MOCK_USER_ID

def test_get_user_id_from_token():
    user_id = get_user_id_from_token(MOCK_TOKEN)
    assert user_id == MOCK_USER_ID

@pytest.mark.parametrize("username,expected", [
    ("valid_user123", True),
    ("invalid user", False),
    ("ab", False),
    ("verylongusernamebeyond30characters", False)
])
def test_validate_username(username, expected):
    assert validate_username(username) == expected

@pytest.mark.parametrize("password,expected", [
    ("StrongP@ssword1", True),
    ("weakpassword", False),
    ("Weak1", False),
    ("Password123", False)
])
def test_validate_password(password, expected):
    assert validate_password(password) == expected

@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("user.example.com", False),
    ("user@", False),
    ("@example.com", False),
])
def test_validate_email(email, expected):
    assert validate_email(email) == expected

@pytest.mark.parametrize("age,expected", [
    (25, True),
    (0, False),
    (-5, False),
    ("25", False)
])
def test_validate_age(age, expected):
    assert validate_age(age) == expected

@pytest.mark.parametrize("gender,expected", [
    ("Male", True),
    ("Female", True),
    ("Other", True),
    ("Unknown", False),
])
def test_validate_gender(gender, expected):
    assert validate_gender(gender) == expected

@pytest.mark.parametrize("status,expected", [
    ("Single", True),
    ("Married", True),
    ("Divorced", True),
    ("Widowed", True),
    ("Complicated", False)
])
def test_validate_marital_status(status, expected):
    assert validate_marital_status(status) == expected

@pytest.mark.parametrize("value,expected", [
    (100.50, True),
    (0.0, False),
    (-50.25, False),
    ("100.50", False)
])
def test_validate_positive_float(value, expected):
    assert validate_positive_float(value) == expected

@pytest.mark.parametrize("value,expected", [
    (10, True),
    (0, False),
    (-5, False),
    ("10", False)
])
def test_validate_positive_int(value, expected):
    assert validate_positive_int(value) == expected
