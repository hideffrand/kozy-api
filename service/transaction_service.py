from datetime import datetime, timezone
from datetime import datetime
from model import Transaction, db, Room, Type, Booking, User
from helper.logger import log
from helper.id_generator import generate_id
import os
from datetime import datetime, timedelta, timezone
here = os.path.basename(__file__)


def get_all_transactions():
    log(here, f"Getting transactions...")
    transactions = Transaction.query.all()

    if not transactions:
        log(here, f"Failed to get transactions")
        return False

    # parsed = []

    # for transaction in transactions:
    #     ts = transaction.to_json()

    #     booking = Booking.query.filter_by(
    #         booking_id=ts.get("booking_id")).first()

    #     if booking:
    #         booking = booking.to_json()
    #         last_payment = booking.get("last_payment")

    #         if last_payment:
    #             if isinstance(last_payment, (datetime, datetime.date)):
    #                 last_payment_date = last_payment
    #             else:
    #                 try:
    #                     last_payment_date = datetime.strptime(
    #                         last_payment, "%a, %d %b %Y %H:%M:%S GMT")
    #                 except ValueError as e:
    #                     log(here,
    #                         f"Error parsing last_payment date for booking {ts['booking_id']}: {e}")
    #                     continue

    #             today = datetime.now(timezone.utc)
    #             days_late = (today - last_payment_date).days

    #             if days_late >= 4:
    #                 if "cost" in ts:
    #                     penalty = 0.10 * ts["cost"]
    #                     ts["penalty"] = penalty
    #                 else:
    #                     log(here,
    #                         f"Missing cost for transaction {ts['booking_id']}, skipping penalty."
    #                     ts["penalty"] = 0
    #             else:
    #                 ts["penalty"] = 0

    #         else:
    #             ts["penalty"] = 0

    #         parsed.append(ts)

    return [transaction.to_json() for transaction in transactions]


def get_all_transactions_by_outlet_id(outlet_id):
    log(here, f"Getting transaction from {outlet_id}...")
    transactions = Transaction.query.filter_by(outlet_id=outlet_id).all()
    if not transactions:
        log(here, f"Failed getting transactions from {outlet_id}")
        return False

    return [transaction.to_json() for transaction in transactions]


def get_all_transactions_by_user_id(user_id):
    log(here, f"Getting transaction from {user_id}...")
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    if not transactions:
        log(here, f"Failed getting transactions from {user_id}")
        return False

    parsed = []
    for transaction in transactions:
        ts = transaction.to_json()

        booking = Booking.query.filter_by(booking_id=ts["booking_id"]).first()
        if booking:
            booking = booking.to_json()
            last_payment = booking.get("last_payment")

            if last_payment:
                last_payment_date = datetime.strptime(
                    last_payment, "%a, %d %b %Y %H:%M:%S GMT")
                today = datetime.now(timezone.utc)

                days_late = (today - last_payment_date).days
                if days_late >= 4:
                    penalty = 0.10 * ts["cost"]
                    ts["penalty"] = penalty
                else:
                    ts["penalty"] = 0

            parsed.append(ts)

    return parsed


def get_transaction_data_by_transaction_id(transaction_id):
    log(here, f"Getting data for user ID {transaction_id}...")
    transaction = Transaction.query.filter_by(
        transaction_id=transaction_id).first()
    if not transaction:
        log(here, f"Transaction with ID {transaction_id} not found.")
        return False

    return transaction.to_json()


def add_new_transaction(transaction_obj):
    log(here, "Adding new transaction...")
    if not transaction_obj:
        log(here, "Invalid transaction data.")
        return False

    log(here, transaction_obj)

    room = Room.query.filter_by(room_id=transaction_obj["room_id"]).first()
    if not room:
        return False
    room = room.to_json()

    room_type = Type.query.filter_by(type_id=room["type_id"]).first()
    if not room_type:
        return False
    room_type = room_type.to_json()

    booking = Booking.query.filter_by(
        booking_id=transaction_obj["booking_id"]).first()
    if not booking:
        return False
    booking = booking.to_json()

    cost = room_type["price"]*booking["stay_duration"]

    new_transaction = Transaction(
        transaction_id=generate_id('T'),
        booking_id=transaction_obj['booking_id'],
        user_id=transaction_obj['user_id'],
        outlet_id=transaction_obj['outlet_id'],
        room_id=transaction_obj['room_id'],
        cost=cost,
        penalty=transaction_obj['penalty'],
        total=cost + transaction_obj['penalty'],
        paid_at=None,
        due_date=transaction_obj['due_date'],
    )

    db.session.add(new_transaction)
    db.session.commit()
    log(here,
        f"New transaction added with ID {new_transaction.transaction_id}.")
    return True


def handle_pay_transaction(transaction_id):
    log(here, f"Updating transaction with ID {transaction_id}...")
    transaction_to_update = Transaction.query.get(transaction_id)
    if not transaction_to_update:
        log(here, f"Transaction with ID {transaction_id} not found.")
        return False

    transaction_to_update.paid_at = datetime.now(timezone.utc)

    transaction = transaction_to_update.to_json()
    room = Room.query.filter_by(
        room_id=transaction["room_id"]).first()
    if not room:
        return False
    room_json = room.to_json()

    user = User.query.filter_by(
        user_id=transaction["user_id"]).first()
    if not user:
        return False
    # user = user.to_json()

    booking = Booking.query.filter_by(
        booking_id=transaction["booking_id"]).first()
    if not booking:
        return False

    booking.last_payment = datetime.now(timezone.utc)
    room.availability_status = False
    user.outlet_id = transaction["outlet_id"]
    user.room_number = room_json["room_number"]

    db.session.commit()
    log(here, f"Transaction with ID {transaction_id} updated.")
    return True


def update_penalty(transaction_id):
    log(here, f"Updating transaction with ID {transaction_id}...")
    transaction_to_update = Transaction.query.get(transaction_id)
    if not transaction_to_update:
        log(here, f"Transaction with ID {transaction_id} not found.")
        return False

    penalty = transaction_to_update.cost/10
    transaction_to_update.penalty += penalty
    transaction_to_update.total += penalty

    transaction = transaction_to_update.to_json()

    user = User.query.filter_by(
        user_id=transaction["user_id"]).first()
    if not user:
        return False

    db.session.commit()
    log(here, f"Transaction with ID {transaction_id} updated.")
    return True


def delete_transaction(transaction_id):
    log(here, f"Deleting transaction with ID {transaction_id}...")
    transaction_to_delete = Transaction.query.get(transaction_id)
    if not transaction_to_delete:
        log(here, f"Transaction with ID {transaction_id} not found.")
        return False

    db.session.delete(transaction_to_delete)
    db.session.commit()
    log(here, f"Transaction with ID {transaction_id} deleted.")
    return True
