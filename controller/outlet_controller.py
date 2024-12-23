from flask import Blueprint, request
from helper.response import send_response
from helper.http_status_code import http_internal_server_error, http_ok, http_method_not_allowed, http_bad_request
from service.outlet_service import search_outlets_by_terms, get_all_outlets, get_outlet_data, get_all_outlet_cities, add_new_outlet

outlets = Blueprint('outlets', __name__)


@outlets.route("/", methods=["GET"])
def get_outlets():
    search_terms = request.args.get('search', None)

    if search_terms:
        data = search_outlets_by_terms(search_terms)
    else:
        data = get_all_outlets()

    if not data:
        send_response(http_internal_server_error)

    return send_response(http_ok, data)


@outlets.route("/<string:id>", methods=["GET"])
def get_one_outlet(id):
    data = get_outlet_data(id)
    if not data:
        send_response(http_internal_server_error)

    return send_response(http_ok, data)


@outlets.route("/cities", methods=["GET"])
def get_outlet_cities():
    data = get_all_outlet_cities()
    if not data:
        send_response(http_internal_server_error)

    return send_response(http_ok, data)


@outlets.route("/", methods=["POST"])
def post_outlets():
    if request.method != 'POST':
        return send_response(http_method_not_allowed)
    body = request.get_json()
    if not body:
        send_response(http_bad_request)

    outlet_obj = {
        "name": body.get('name'),
        "address": body.get("address"),
        "phone": body.get("phone"),
        "spv_id": body.get("spv_id"),
        "type_teratas": body.get("type_teratas"),
        "motorcycle_slot": body.get("motorcycle_slot"),
        "car_slot": body.get("car_slot"),
    }

    new_outlet = add_new_outlet(outlet_obj)
    if not new_outlet:
        send_response(http_bad_request)

    return send_response(http_ok, 'OK')

@outlets.route("/customers", methods=['GET'])
def get_outlet_customers():
    return send_response()