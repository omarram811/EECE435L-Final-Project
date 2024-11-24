import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your_secret_key"
TOKEN_EXPIRATION_MINUTES = 30

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def get_user_id_from_token(token):
    payload = verify_token(token)
    if "user_id" in payload:
        return payload["user_id"]
    return None
