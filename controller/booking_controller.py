from flask import Blueprint, request
from flask_cors import cross_origin
from helper.response import send_response
from helper.http_status_code import http_internal_server_error, http_ok, http_bad_request, http_method_not_allowed
from service.booking_service import get_user_booking, get_outlet_booking, get_all_bookings, update_booking_data, add_new_booking, cancel_booking_after_4_days
from helper.http_status_code import http_not_found
bookings = Blueprint('bookings', __name__)


@bookings.route("/", methods=["GET"])
def get_bookings():
    user_id = request.args.get("user_id")
    outlet_id = request.args.get("outlet_id")

    if user_id:
        data = get_user_booking(user_id)
    elif outlet_id:
        data = get_outlet_booking(outlet_id)
    else:
        data = get_all_bookings()
    if not data:
        return send_response(http_internal_server_error)

    return send_response(http_ok, data)


@bookings.route("/cancel/<string:booking_id>", methods=["GET"])
def cancel_booking_all(booking_id):
    if not booking_id:
        return send_response(http_bad_request)

    res = cancel_booking_after_4_days(booking_id)
    if not res:
        return send_response(http_internal_server_error)

    return send_response(http_ok)

# @bookings.route("/<string:id>", methods=["GET"])
# def get_one_bookings(id):
#     data = get_booking_data(id)
#     if not data:
#         send_response(http_internal_server_error)

#     return send_response(http_ok, data)


@bookings.route("/", methods=["PUT"])
def update_one_booking():
    if request.method != 'PUT':
        return send_response(http_method_not_allowed)

    body = request.get_json()
    if not body:
        return send_response(http_bad_request)

    updated = update_booking_data(body.get("booking_id"), body.get("accepted"))
    if not updated:
        send_response(http_internal_server_error)

    return send_response(http_ok)


@bookings.route("/", methods=["POST"])
def post_booking():
    body = request.get_json()
    if not body:
        send_response(http_bad_request)
    json = {
        "room_id": body.get("room_id"),
        "outlet_id": body.get("outlet_id"),
        "user_id": body.get("user_id"),
        "check_in_date": body.get("check_in_date"),
        "stay_duration": body.get("stay_duration")
    }
    result = add_new_booking(json)
    if not result:
        return send_response(http_internal_server_error)
    return send_response(http_ok)
