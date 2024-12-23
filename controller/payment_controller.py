from flask import Blueprint, request
from helper.response import send_response
from helper.http_status_code import http_bad_request, http_internal_server_error, http_method_not_allowed, http_ok  
from service.payment_service import get_all_payments, get_some_payments, add_new_payment

payments = Blueprint('payments', __name__)


@payments.route("/", methods=["GET"])
def get_payments():
    data = get_all_payments()
    if not data:
        send_response(http_internal_server_error)

    return send_response(http_ok, data)


@payments.route("/", methods=["POST"])
def post_payments():
    if request.method != 'POST':
        return send_response(http_method_not_allowed)
    body = request.get_json()
    if not body:
        send_response(http_bad_request)

    payment_obj = {
        "timestamp": body.get('timestamp'),
        "via": body.get('via'),
        "proof": body.get('proof'),
        "water": body.get('water'),
        "wifi": body.get('wifi'),
        "electricity": body.get('electricity'),
        "spv_payroll": body.get('spv_payroll'),
        "additional": body.get('additional'),
        "total": body.get('total'),
    }

    new_payment = add_new_payment(payment_obj)
    if not new_payment:
        send_response(http_bad_request)

    return send_response(http_ok, 'OK')
