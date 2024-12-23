from model import Payment, db
from helper.logger import log
from helper.id_generator import generate_id
from datetime import datetime
import os
here = os.path.basename(__file__)

def get_all_payments():
    log(here, "Fetching all payments...")

    try:
        # Fetch all payment records
        payments = Payment.query.all()
        if not payments:
            log(here, "No payments found.")
            return []

        # Build the response
        response = []
        for payment in payments:
            response.append({
                "payment_id": payment.payment_id,
                "timestamp": payment.timestamp.strftime('%Y-%m-%d') if payment.timestamp else None,
                "via": payment.via,
                "proof": payment.proof.decode('utf-8') if payment.proof else None,
                "water": payment.water,
                "wifi": payment.wifi,
                "electricity": payment.electricity,
                "spv_payroll": payment.spv_payroll,
                "additional": payment.additional,
                "total": payment.total,
            })

        log(here, f"Successfully fetched {len(payments)} payments.")
        return response
    except Exception as e:
        log(here, f"Error fetching payments: {e}")
        return False

def get_some_payments(start, end):
    log(here, f"Fetching payments between {start} and {end}...")
    
    try:
        # Convert string dates to datetime if they're strings
        if isinstance(start, str):
            start = datetime.strptime(start, '%Y-%m-%d')
        if isinstance(end, str):
            end = datetime.strptime(end, '%Y-%m-%d')
        
        # Fetch payments within date range
        payments = Payment.query.filter(
            Payment.timestamp >= start,
            Payment.timestamp <= end
        ).all()
        
        if not payments:
            log(here, "No payments found in the specified date range.")
            return []
        
        # Build the response
        response = []
        for payment in payments:
            response.append({
                "payment_id": payment.payment_id,
                "timestamp": payment.timestamp.strftime('%Y-%m-%d') if payment.timestamp else None,
                "via": payment.via,
                "proof": payment.proof.decode('utf-8') if payment.proof else None,
                "water": payment.water,
                "wifi": payment.wifi,
                "electricity": payment.electricity,
                "spv_payroll": payment.spv_payroll,
                "additional": payment.additional,
                "total": payment.total,
            })
        
        log(here, f"Successfully fetched {len(payments)} payments for the specified date range.")
        return response
        
    except ValueError as ve:
        log(here, f"Error parsing dates: {ve}")
        return False
    except Exception as e:
        log(here, f"Error fetching payments: {e}")
        return False

def add_new_payment(payment_obj):
    log(here, "Adding new payment...")

    # Validate input
    if not payment_obj or not isinstance(payment_obj, dict):
        log(here, "Invalid payment object. Failed adding new payment.")
        return False

    try:
        # Create a new Payment instance
        new_payment = Payment(
            payment_id=generate_id('P'),
            timestamp=payment_obj.get("timestamp"),
            via=payment_obj.get("via"),
            proof=payment_obj.get("proof"),
            water=payment_obj.get("water"),
            wifi=payment_obj.get("wifi"),
            electricity=payment_obj.get("electricity"),
            spv_payroll=payment_obj.get("spv_payroll"),
            additional=payment_obj.get("additional"),
            total=payment_obj.get("total"),
        )

        # Add to the database session and commit
        db.session.add(new_payment)
        db.session.commit()
        log(here, "New payment added successfully!")
        return True
    except Exception as e:
        log(here, f"Error adding new payment: {e}")
        return False


def update_payment(payment_id, payment_obj):
    log(here, "Updating payment...")

    if not payment_obj or not isinstance(payment_obj, dict):
        log(here, "Invalid payment object. Failed updating payment.")
        return False

    try:
        # Find the payment by ID
        payment_to_update = Payment.query.get(payment_id)
        if not payment_to_update:
            log(here, f"Payment with ID {payment_id} not found.")
            return False

        # Update payment attributes dynamically
        for key, value in payment_obj.items():
            if hasattr(payment_to_update, key):
                setattr(payment_to_update, key, value)

        # Commit the changes
        db.session.commit()
        log(here, f"Payment with ID {payment_id} updated successfully!")
        return True
    except Exception as e:
        log(here, f"Error updating payment: {e}")
        return False


def delete_payment(payment_id):
    log(here, "Deleting payment...")

    try:
        # Find the payment by ID
        payment_to_delete = Payment.query.get(payment_id)
        if not payment_to_delete:
            log(here, f"Payment with ID {payment_id} not found.")
            return False

        # Delete the payment
        db.session.delete(payment_to_delete)
        db.session.commit()
        log(here, f"Payment with ID {payment_id} deleted successfully!")
        return True
    except Exception as e:
        log(here, f"Error deleting payment: {e}")
        return False
