import re

def validate_username(username):
    if not username or len(username) < 3 or len(username) > 30 or " " in username:
        return False
    return True

def validate_password(password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def validate_age(age):
    return isinstance(age, int) and age > 0

def validate_gender(gender):
    return gender in ["Male", "Female", "Other"]

def validate_marital_status(status):
    return status in ["Single", "Married", "Divorced", "Widowed"]

def validate_positive_float(value):
    return isinstance(value, float) and value > 0

def validate_positive_int(value):
    return isinstance(value, int) and value > 0
