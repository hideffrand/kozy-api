import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app, request
from helper.http_status_code import *
import bcrypt

VERY_SECRET_KEY = 'VERY_SECRET_KEY'


def generate_token(user):
    payload = {
        'sub': user['email'],
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=12)
    }
    token = jwt.encode(payload, VERY_SECRET_KEY, algorithm='HS256')

    return token


def decode_token(token):
    decoded_token = jwt.decode(token, VERY_SECRET_KEY, algorithms=['HS256'])
    if not decoded_token:
        return False

    return decoded_token


def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
