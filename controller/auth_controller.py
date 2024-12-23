from flask import Blueprint, request, session
from helper.response import send_response
from helper.http_status_code import http_internal_server_error, http_method_not_allowed, http_bad_request, http_ok, http_created, http_not_found
from service.user_service import login, register, get_user_data_by_email
from service.auth_service import generate_token, decode_token
from helper.logger import log
import os
from datetime import datetime, timedelta

here = os.path.basename(__file__)
auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['POST'])
def auth_login():
    if request.method != 'POST':
        return send_response(http_method_not_allowed)

    log(here, "New Login Request")
    body = request.get_json()
    if body is None:
        log(here, "Failed Login Request")
        return send_response(http_bad_request)

    user_obj = {
        'email': body.get("email"),
        'password': body.get("password")
    }

    user = login(user_obj)
    if not user:
        return send_response(http_internal_server_error)

    del user['password']

    token = generate_token(user_obj)
    response = send_response(http_ok, {"user": user, "token": token})
    # expires = datetime.now() + timedelta(hours=6)
    # response.set_cookie('token', token, expires=expires, httponly=True)
    return response


@auth.route("/register", methods=['POST'])
def auth_register():
    if request.method != 'POST':
        return send_response(http_method_not_allowed)

    log(here, "New Register Request")

    body = request.get_json()
    if body is None:
        log(here, "Failed Register Request")
        return send_response(http_bad_request)

    user_obj = {
        'email': body.get("email"),
        'password': body.get("password"),
        'name': body.get("name"),
        "address": body.get("address"),
    }

    new_user = register(user_obj)
    if not new_user:
        return send_response(http_internal_server_error)

    del new_user['password']

    token = generate_token(new_user)
    response = send_response(http_created, {'user': new_user, 'token': token})
    # expires = datetime.now() + timedelta(hours=6)
    # response.set_cookie('token', token, expires=expires, httponly=True)
    return response


@auth.route("/logout", methods=['POST'])
def auth_logout():
    response = send_response(http_ok, 'Logged out successfully')
    response.delete_cookie('token')

    return response


@auth.route("/test-cookie", methods=['GET', 'POST'])
def test_cookie():
    token = request.cookies.get('token')
    if not token:
        return send_response(http_not_found, None)

    parsed_token = decode_token(token)
    role = get_user_data_by_email(parsed_token.get('email'))

    return send_response(http_ok, 'ada')
