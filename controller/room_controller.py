from flask import Blueprint, request
from helper.response import send_response
from helper.http_status_code import http_internal_server_error, http_ok, http_bad_request, http_method_not_allowed
from service.room_service import get_all_rooms, get_room_data, get_all_types, get_type_data, add_new_room

rooms = Blueprint('rooms', __name__)


@rooms.route("/", methods=["GET"])
def get_rooms():
    data = get_all_rooms()
    if not data:
        send_response(http_internal_server_error)

    return send_response(http_ok, data)


@rooms.route("/<string:id>", methods=["GET"])
def get_one_room(id):
    data = get_room_data(id)
    if not data:
        send_response(http_internal_server_error)
        
    return send_response(http_ok, data)


@rooms.route("/types", methods=["GET"])
def get_room_types():
    data = get_all_types()
    if not data:
        send_response(http_internal_server_error)

    return send_response(http_ok, data)


@rooms.route("/types/<string:id>", methods=["GET"])
def get_type(id):
    data = get_type_data(id)
    if not data:
        send_response(http_internal_server_error)

    return send_response(http_ok, data)


@rooms.route("/", methods=["POST"])
def post_rooms():
    if request.method != 'POST':
        return send_response(http_method_not_allowed)
    body = request.get_json()
    if not body:
        send_response(http_bad_request)

    room_obj = {
        "room": body.get('room'),
        "type_id": body.get('type_id'),
        "outlet_id": body.get('outlet_id'),
        "size": body.get('size'),
        "price": body.get('price'),
        "photo": body.get('photo'),
        "availability_status": body.get('availability_status'),
    }

    new_room = add_new_room(room_obj)
    if not new_room:
        send_response(http_bad_request)

    return send_response(http_ok, 'OK')
