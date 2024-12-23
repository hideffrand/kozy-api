from flask import Blueprint, request
from flask_cors import cross_origin
from helper.response import send_response
from helper.http_status_code import *
from helper.logger import log
from service.transaction_service import *
import os
here = os.path.basename(__file__)
transactions = Blueprint('transactions', __name__)


@transactions.route("/", methods=['GET'])
def get_transactions():
    user_id = request.args.get("user_id")
    outlet_id = request.args.get("outlet_id")

    if user_id:
        data = get_all_transactions_by_user_id(user_id)
    elif outlet_id:
        data = get_all_transactions_by_outlet_id(outlet_id)
    else:
        data = get_all_transactions()
    if not data:
        return send_response(http_internal_server_error)

    return send_response(http_ok, data)


@transactions.route("/", methods=['POST'])
def post_transaction():
    body = request.get_json()
    if not body:
        return send_response(http_bad_request)

    transaction_obj = {
        "booking_id": body.get("booking_id"),
        "user_id": body.get("user_id"),
        "outlet_id": body.get("outlet_id"),
        "room_id": body.get("room_id"),
        # "cost": body.get("cost"),
        "penalty": body.get("penalty"),
        # "total": body.get("total"),
        "due_date": body.get("due_date")
    }

    data = add_new_transaction(transaction_obj)
    if not data:
        return send_response(http_internal_server_error)

    return send_response(http_ok)


@transactions.route("/<transaction_id>/penalty", methods=["POST"])
def apply_penalty(transaction_id):
    log(here, f"Handling PUT /transaction/{transaction_id}")

    result = update_penalty(transaction_id)
    if not result:
        return send_response(http_not_found, f"Failed to update transaction record with ID {transaction_id}.")
    return send_response(http_ok, f"transaction record with ID {transaction_id} updated successfully.")


@transactions.route("/<transaction_id>/pay", methods=["POST"])
def update_transaction_record(transaction_id):
    log(here, f"Handling PUT /transaction/{transaction_id}")

    result = handle_pay_transaction(transaction_id)
    if not result:
        return send_response(http_not_found, f"Failed to update transaction record with ID {transaction_id}.")
    return send_response(http_ok, f"transaction record with ID {transaction_id} updated successfully.")
