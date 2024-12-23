from model import Booking, db, Room, User
from helper.logger import log
from helper.id_generator import generate_id
import os
here = os.path.basename(__file__)


def cancel_booking_after_4_days(booking_id):
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if not booking:
        return False
    booking_json = booking.to_json()

    user = User.query.filter_by(user_id=booking_json["user_id"]).first()
    room = Room.query.filter_by(room_id=booking_json["room_id"]).first()

    user.room_number = None
    user.outlet_id = None
    room.availability_status = False
    booking.accepted = False
    db.session.commit()

    return True


def get_booking_data(booking_id):
    log(here, 'Getting booking data....')

    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if not booking:
        log(here, 'Failed getting booking datas.')
        return False

    booking.to_json()

    return booking


def get_user_booking(user_id):
    log(here, 'Getting booking data....')

    bookings = Booking.query.filter_by(user_id=user_id).all()
    if not bookings:
        log(here, 'Failed getting booking datas.')
        return False

    return [booking.to_json() for booking in bookings]


def get_outlet_booking(outlet_id):
    log(here, 'Getting booking data....')

    booking = Booking.query.filter_by(outlet_id=outlet_id).all()
    if not booking:
        log(here, 'Failed getting booking datas.')
        return False

    booking.to_json()

    return booking


def update_booking_data(booking_id, accepted_value):
    log(here, 'Updating booking data...')

    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if not booking:
        log(here, 'Booking not found.')
        return False

    if not isinstance(accepted_value, bool):
        log(here, 'Invalid accepted value. Must be a boolean.')
        return False

    booking.accepted = accepted_value
    db.session.commit()
    log(here,
        f'Booking {booking_id} updated successfully to {accepted_value}.')
    return True


def get_all_bookings():
    log(here, "Fetching all bookings...")

    try:
        # Fetch all booking records
        bookings = Booking.query.all()
        if not bookings:
            log(here, "No bookings found.")
            return []

        # Build the response
        response = []
        for booking in bookings:
            response.append({
                "booking_id": booking.booking_id,
                "room_id": booking.room_id,
                "outlet_id": booking.outlet_id,
                "user_id": booking.user_id,
                "check_in_date": booking.check_in_date.strftime('%Y-%m-%d') if booking.check_in_date else None,
                "stay_duration": booking.stay_duration,
                "accepted": booking.accepted,
            })

        log(here, f"Successfully fetched {len(bookings)} bookings.")
        return response
    except Exception as e:
        log(here, f"Error fetching bookings: {e}")
        return False


def add_new_booking(json):
    log(here, "Adding new booking...")

    # Validate input
    if not json or not isinstance(json, dict):
        log(here, "Invalid booking object. Failed adding new booking.")
        return False

    try:
        # Create a new Booking instance
        new_booking = Booking(
            booking_id=generate_id('B'),
            room_id=json["room_id"],
            outlet_id=json["outlet_id"],
            user_id=json["user_id"],
            check_in_date=json["check_in_date"],
            stay_duration=json["stay_duration"],
            accepted=None,
            last_payment=None
        )

        db.session.add(new_booking)
        db.session.commit()
        log(here, "New booking added successfully!")
        return True
    except Exception as e:
        log(here, f"Error adding new booking: {e}")
        return False


def update_booking(booking_id, booking_obj):
    log(here, "Updating booking...")

    if not booking_obj or not isinstance(booking_obj, dict):
        log(here, "Invalid booking object. Failed updating booking.")
        return False

    try:
        # Find the booking by ID
        booking_to_update = Booking.query.get(booking_id)
        if not booking_to_update:
            log(here, f"Booking with ID {booking_id} not found.")
            return False

        # Update booking attributes dynamically
        for key, value in booking_obj.items():
            if hasattr(booking_to_update, key):
                setattr(booking_to_update, key, value)

        # Commit the changes
        db.session.commit()
        log(here, f"Booking with ID {booking_id} updated successfully!")
        return True
    except Exception as e:
        log(here, f"Error updating booking: {e}")
        return False


def delete_booking(booking_id):
    log(here, "Deleting booking...")

    try:
        # Find the booking by ID
        booking_to_delete = Booking.query.get(booking_id)
        if not booking_to_delete:
            log(here, f"Booking with ID {booking_id} not found.")
            return False

        # Delete the booking
        db.session.delete(booking_to_delete)
        db.session.commit()
        log(here, f"Booking with ID {booking_id} deleted successfully!")
        return True
    except Exception as e:
        log(here, f"Error deleting booking: {e}")
        return False
