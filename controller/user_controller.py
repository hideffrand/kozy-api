from flask import Blueprint, request
from helper.response import send_response
from helper.http_status_code import http_not_found, http_ok, http_bad_request
from service.user_service import get_all_users, update_user, get_user_data
from helper.logger import log
import os
here = os.path.basename(__file__)
users = Blueprint('users', __name__)


@users.route("/", methods=['GET'])
def get_users():
    role = request.args.get('role')
    outlet_id = request.args.get('outlet_id')
    data = get_all_users(role)
    if not data or data == '':
        return send_response(http_not_found, None)

    return send_response(http_ok, data)


@users.route("/<user_id>", methods=["PUT"])
def update_user_record(user_id):
    log(here, f"Handling PUT /user/{user_id}")
    body = request.get_json()
    if not body:
        return send_response(http_bad_request, "Invalid request body.")

    result = update_user(user_id, body)
    if not result:
        return send_response(http_not_found, f"Failed to update user record with ID {user_id}.")
    return send_response(http_ok, f"user record with ID {user_id} updated successfully.")


@users.route("/<string:id>", methods=['GET'])
def get_user(id):
    data = get_user_data(id)
    if not data:
        return send_response(http_not_found, 'User not found')

    del data['password']

    return send_response(http_ok, data)
