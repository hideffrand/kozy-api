from flask import Flask, request
from controller.room_controller import rooms
from controller.auth_controller import auth
from controller.outlet_controller import outlets
from controller.payment_controller import payments
from controller.user_controller import users
from controller.booking_controller import bookings
from controller.report_controller import report
from controller.maintenance_controller import maintenance
from controller.transaction_controller import transactions
from service.user_service import generate_spvs
from service.outlet_service import generate_outlets
from service.room_service import generate_types, generate_rooms
from helper.logger import log
from helper.response import send_response
from helper.http_status_code import http_ok
from flask_cors import CORS
from model import db
import os
from dotenv import load_dotenv

load_dotenv()
here = os.path.basename(__file__)
app = Flask(__name__)
CORS(app,
     origins=["http://localhost:5174",
              "https://p9jctgvq-5174.asse.devtunnels.ms"],
     methods=["GET", "POST", "PUT", "PATCH"]
     )


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI_POSTGRE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.before_request
def check_if_options():
    if request.method == 'OPTIONS':
        return '', 200  # Allow the preflight request without authentication


@app.route("/", methods=["GET"])
def index():
    return send_response(http_ok, 'ok')


@app.route("/api/test", methods=["GET"])
def api_test():
    return send_response(http_ok, 'ok')


# HATI HATI PAKE INI HARUS DROP TABEL DULU
@app.route("/api/generate", methods=["GET"])
def generate_all():
    log(here, "Generating data...")
    generate_spvs()
    generate_outlets()
    generate_types()
    generate_rooms()
    log(here, "Success generating data.")
    return send_response(http_ok, 'Generated')


@app.route("/api", methods=["GET"])
def api_service():
    return send_response(http_ok, 'Halo')


app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(users, url_prefix='/api/users')
app.register_blueprint(rooms, url_prefix='/api/rooms')
app.register_blueprint(outlets, url_prefix='/api/outlets')
app.register_blueprint(payments, url_prefix='/api/payments')
app.register_blueprint(bookings, url_prefix='/api/bookings')
app.register_blueprint(transactions, url_prefix='/api/transactions')
app.register_blueprint(maintenance, url_prefix='/api/maintenance')
app.register_blueprint(report, url_prefix='/api/report')


if __name__ == '__main__':
    log(here, 'App running.')
    app.run(debug=os.getenv('DEBUG'), port=5050)
