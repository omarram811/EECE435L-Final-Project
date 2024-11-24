"""
Authentication Module
---------------------
This module provides utilities for generating and verifying JSON Web Tokens (JWT)
for user authentication and extracting user information from tokens.

Constants:
----------
SECRET_KEY : str
    The secret key used for encoding and decoding JWT tokens.
TOKEN_EXPIRATION_MINUTES : int
    The duration (in minutes) for which the token remains valid.

Functions:
----------
- generate_token(user_id: int) -> str
    Generates a JWT token for a given user ID.
- verify_token(token: str) -> dict
    Verifies a JWT token and decodes its payload.
- get_user_id_from_token(token: str) -> Optional[int]
    Extracts the user ID from the provided JWT token.
"""

import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your_secret_key"
TOKEN_EXPIRATION_MINUTES = 30

def generate_token(user_id):
    """
    Generates a JWT token for a given user ID.

    Parameters:
    ----------
    user_id : int
        The unique identifier of the user.

    Returns:
    -------
    str
        A signed JWT token with encoded user ID and expiration.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    """
    Verifies a JWT token and decodes its payload.

    Parameters:
    ----------
    token : str
        The JWT token to verify.

    Returns:
    -------
    dict
        The decoded payload if the token is valid, or an error message.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def get_user_id_from_token(token):
    """
    Extracts the user ID from the provided JWT token.

    Parameters:
    ----------
    token : str
        The JWT token from which the user ID is to be extracted.

    Returns:
    -------
    Optional[int]
        The user ID if successfully extracted; otherwise, None.
    """
    payload = verify_token(token)
    if "user_id" in payload:
        return payload["user_id"]
    return None
