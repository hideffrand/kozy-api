from model import Maintenance, db
from helper.logger import log
from helper.id_generator import generate_id
import os
from datetime import datetime, timedelta, timezone

here = os.path.basename(__file__)


def get_maintenance_data(maintenance_id):
    log(here, 'Getting maintenance data...')

    maintenance = Maintenance.query.filter_by(
        maintenance_id=maintenance_id).first()
    if not maintenance:
        log(here, 'Failed to get maintenance data.')
        return False

    # Assuming `to_json` is defined in the `Maintenance` model
    return maintenance.to_json()


def get_all_maintenance():
    log(here, "Fetching all maintenance records...")
    maintenances = Maintenance.query.all()
    if not maintenances:
        return False

    return [maintenance.to_json() for maintenance in maintenances]


def get_all_maintenance_by_user_id(user_id):
    log(here, "Fetching all maintenance records...")
    maintenances = Maintenance.query.filter_by(user_id=user_id).all()
    if not maintenances:
        return False

    return [maintenance.to_json() for maintenance in maintenances]


def get_all_maintenance_by_outlet(outlet_id):
    log(here, "Fetching all maintenance records...")
    maintenances = Maintenance.query.filter_by(outlet_id=outlet_id).all()
    if not maintenances:
        return False

    return [maintenance.to_json() for maintenance in maintenances]


def add_new_maintenance(maintenance_obj):
    log(here, "Adding new maintenance record...")

    if not maintenance_obj or not isinstance(maintenance_obj, dict):
        log(here, "Invalid maintenance object. Failed to add new record.")
        return False

    try:
        # Create a new Maintenance instance
        new_maintenance = Maintenance(
            maintenance_id=generate_id('M'),
            outlet_id=maintenance_obj.get("outlet_id"),
            room_number=maintenance_obj.get("room_number"),
            user_id=maintenance_obj.get("user_id"),
            issue=maintenance_obj.get("issue"),
            date_reported=datetime.now(timezone.utc),
            status='sent',
            resolution_date=None,
        )

        # Add to the database session and commit
        db.session.add(new_maintenance)
        db.session.commit()
        log(here, "New maintenance record added successfully!")
        return True
    except Exception as e:
        log(here, f"Error adding maintenance record: {e}")
        return False


def update_maintenance(maintenance_id, maintenance_obj):
    log(here, "Updating maintenance record...")

    if not maintenance_obj or not isinstance(maintenance_obj, dict):
        log(here, "Invalid maintenance object. Failed to update record.")
        return False

    try:
        # Find the maintenance record by ID
        maintenance_to_update = Maintenance.query.get(maintenance_id)
        if not maintenance_to_update:
            log(here,
                f"Maintenance record with ID {maintenance_id} not found.")
            return False

        # Update maintenance attributes dynamically
        for key, value in maintenance_obj.items():
            if hasattr(maintenance_to_update, key):
                setattr(maintenance_to_update, key, value)

        # Commit the changes
        db.session.commit()
        log(here,
            f"Maintenance record with ID {maintenance_id} updated successfully!")
        return True
    except Exception as e:
        log(here, f"Error updating maintenance record: {e}")
        return False


def delete_maintenance(maintenance_id):
    log(here, "Deleting maintenance record...")

    try:
        # Find the maintenance record by ID
        maintenance_to_delete = Maintenance.query.get(maintenance_id)
        if not maintenance_to_delete:
            log(here,
                f"Maintenance record with ID {maintenance_id} not found.")
            return False

        # Delete the maintenance record
        db.session.delete(maintenance_to_delete)
        db.session.commit()
        log(here,
            f"Maintenance record with ID {maintenance_id} deleted successfully!")
        return True
    except Exception as e:
        log(here, f"Error deleting maintenance record: {e}")
        return False
