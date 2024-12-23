from flask import Blueprint, request
from helper.response import send_response
from helper.http_status_code import http_internal_server_error, http_not_found, http_ok, http_bad_request, http_created
from service.maintenance_service import *
import os
maintenance = Blueprint('maintenance', __name__)
here = os.path.basename(__file__)


@maintenance.route("/", methods=["GET"])
def get_all_maintenances():
    user_id = request.args.get("user_id")
    outlet_id = request.args.get("outlet_id")
    if user_id:
        data = get_all_maintenance_by_user_id(user_id)
    elif outlet_id:
        data = get_all_maintenance_by_outlet(outlet_id)
    else:
        data = get_all_maintenance()

    if not data:
        return send_response(http_not_found)
    
    return send_response(http_ok, data)


@maintenance.route("/<string:maintenance_id>", methods=["GET"])
def get_maintenance_by_id(maintenance_id):
    data = get_maintenance_data(maintenance_id)
    if not data:
        return send_response(http_not_found, f"Maintenance record with ID {maintenance_id} not found.")
    return send_response(http_ok, data)


@maintenance.route("/", methods=["POST"])
def add_maintenance():
    log(here, "Handling POST /maintenance")
    body = request.get_json()
    if not body:
        return send_response(http_bad_request, "Invalid request body.")

    maintenance_obj = {
        "outlet_id": body.get("outlet_id"),
        "room_number": body.get("room_number"),
        "user_id": body.get("user_id"),
        "issue": body.get("issue"),
    }

    result = add_new_maintenance(maintenance_obj)
    if not result:
        return send_response(http_internal_server_error, "Failed to add maintenance record.")
    return send_response(http_created, "New maintenance record added successfully.")


@maintenance.route("/<maintenance_id>", methods=["PUT"])
def update_maintenance_record(maintenance_id):
    log(here, f"Handling PUT /maintenance/{maintenance_id}")
    body = request.get_json()
    if not body:
        return send_response(http_bad_request, "Invalid request body.")

    result = update_maintenance(maintenance_id, body)
    if not result:
        return send_response(http_not_found, f"Failed to update maintenance record with ID {maintenance_id}.")
    return send_response(http_ok, f"Maintenance record with ID {maintenance_id} updated successfully.")


@maintenance.route("/<maintenance_id>", methods=["DELETE"])
def delete_maintenance_record(maintenance_id):
    log(here, f"Handling DELETE /maintenance/{maintenance_id}")
    result = delete_maintenance(maintenance_id)
    if not result:
        return send_response(http_not_found, f"Failed to delete maintenance record with ID {maintenance_id}.")
    return send_response(http_ok, f"Maintenance record with ID {maintenance_id} deleted successfully.")
