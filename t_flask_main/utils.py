import jwt
from datetime import datetime, timedelta
from t_flask import app

SECRET_KEY = app.config.get('SECRET_KEY', 'default_secret')

def generate_token(user_id, expires_sec=120):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_sec)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    from t_flask.models import User
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return User.query.get(payload["user_id"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
