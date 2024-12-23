from flask import Blueprint, request
from helper.response import send_response
from helper.http_status_code import http_ok
from service.payment_service import get_some_payments
from service.maintenance_service import get_all_maintenance
from service.transaction_service import *

report = Blueprint('report', __name__)

@report.route("/", methods=["GET"])
def get_report(start,end):
    data = {
        "payment": get_some_payments(start,end),
        "maintenance": get_all_maintenance()
    }
    return send_response(http_ok, data)