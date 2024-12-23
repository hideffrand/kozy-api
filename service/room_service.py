from model import Room, Type, Outlet, db
from helper.logger import log
from helper.id_generator import generate_id
import os
here = os.path.basename(__file__)


def get_all_rooms():
    log(here, "Getting rooms data...")
    rooms = Room.query.all()
    if not rooms:
        log(here, "Failed getting rooms data")
        return False

    return [room.to_json() for room in rooms]


def get_outlet_rooms(outlet_id):
    log(here, 'Getting outlet rooms....')
    """
    Since room save outlet_id,  we can
    get all the room from an outlet.
    Then we iterate each room to get the
    detail of each type
    """
    rooms = Room.query.filter_by(outlet_id=outlet_id).all()
    if not rooms:
        log(here, 'Failed getting outlet rooms.')
        return False

    rooms = [room.to_json() for room in rooms]
    for room in rooms:
        type_data = get_type_data(room["type_id"])
        room["price"] = type_data["price"]
        room["size"] = type_data["size"]
        room["type_name"] = type_data["type_name"]
    return rooms


def get_room_data(room_id):
    log(here, 'Getting room datas....')
    """
    Since room save room_id,  we can
    get all the type data from an room.
    Then we iterate each room to get the
    detail of each type
    """
    room = Room.query.filter_by(room_id=room_id).first()
    if not room:
        log(here, 'Failed getting room datas.')
        return False

    room = room.to_json()
    room["type_desc"] = get_type_data(room["type_id"])
    return room


def add_new_room(room_obj):
    log(here, "Adding new room...")
    if room_obj != {}:
        log(here, "Failed adding new room...")
        return False

    new_room = Room(
        generate_id('R'),
        room_obj["type_id"],
        room_obj["outlet_id"],
        room_obj["size"],
        room_obj["price"],
        room_obj["photo"],
        room_obj["availability_status"]
    )
    db.session.add(new_room)
    db.session.commit()
    log(here, "New Room Added!")
    return True


def update_room(room_id, room_obj):
    log(here, "Updating room...")

    room_to_update = Room.query.get(room_id)
    if not room_to_update:
        log(here, f"Room with ID {room_id} not found.")
        return False

    if 'type_id' in room_obj:
        room_to_update.type_id = room_obj["type_id"]
    if 'outlet_id' in room_obj:
        room_to_update.outlet_id = room_obj["outlet_id"]
    if 'size' in room_obj:
        room_to_update.size = room_obj["size"]
    if 'price' in room_obj:
        room_to_update.price = room_obj["price"]
    if 'photo' in room_obj:
        room_to_update.photo = room_obj["photo"]
    if 'availability_status' in room_obj:
        room_to_update.availability_status = room_obj["availability_status"]

    db.session.commit()
    log(here, f"Room with ID {room_id} updated!")
    return True


def delete_room(room_id):
    log(here, "Deleting room...")

    room_to_delete = Room.query.get(room_id)
    if not room_to_delete:
        log(here, f"Room with ID {room_id} not found.")
        return False

    db.session.delete(room_to_delete)
    db.session.commit()
    log(here, f"Room with ID {room_id} deleted!")
    return True


def get_all_types():
    log(here, 'Getting types...')

    room_types = db.session.query(Type).all()
    if not room_types:
        log(here, "Failed getting types")
        return False

    return [t.to_json() for t in room_types]


def get_type_data(id):
    log(here, "Getting type data...")

    type_data = Type.query.filter_by(type_id=id).first()
    if not type_data:
        log(here, "Failed getting types data")
        return False

    return type_data.to_json()


def generate_types():
    log(here, 'Generating types...')
    types = [
        Type(
            type_id="1",
            type_name="Luxury",
            bathroom=True,
            ac=True,
            tv=True,
            wifi_speed=90,
            mini_pantry=True,
            dispenser=True,
            fridge=True,
            size='5m x 5m',
            price=3_750_000
        ),
        Type(
            type_id="2",
            type_name="Deluxe",
            bathroom=True,
            ac=True,
            tv=True,
            wifi_speed=60,
            mini_pantry=True,
            dispenser=True,
            fridge=True,
            size='5m x 4m',
            price=3_000_000
        ),
        Type(
            type_id="3",
            type_name="Superior",
            bathroom=True,
            ac=True,
            tv=False,
            wifi_speed=40,
            mini_pantry=False,
            dispenser=True,
            fridge=True,
            size='4m x 4m',
            price=2_000_000
        ),
        Type(
            type_id="4",
            type_name="Standard",
            bathroom=False,
            ac=True,
            tv=False,
            wifi_speed=20,
            mini_pantry=False,
            dispenser=True,
            fridge=True,
            size='3m x 3m',
            price=1_400_000
        ),
        Type(
            type_id="5",
            type_name="Economic",
            bathroom=False,
            ac=False,
            tv=False,
            wifi_speed=10,
            mini_pantry=False,
            dispenser=False,
            fridge=False,
            size='2,5m x 2,5m',
            price=750_000
        ),
    ]

    for t in types:
        db.session.add(t)
        db.session.commit()

    log(here, 'Types generated.')


def generate_rooms():
    log(here, "Generating Rooms...")
    outlets = db.session.query(Outlet).all()
    parsed_outlet = [outlet.to_json() for outlet in outlets]
    placeholder = "https://placehold.co/300x300?text=Room"

    room_types_pairs = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5)
    ]

    for i in range(20):
        type_1, type_2 = room_types_pairs[i]

        # Generate 3 kamar untuk tipe pertama (type_1)
        for j in range(3):
            db.session.add(Room(
                room_id=generate_id('R'),
                room_number=j + 1,
                type_id=type_1,
                outlet_id=parsed_outlet[i]["outlet_id"],
                photo=placeholder,
                availability_status=True
            ))
            db.session.commit()

        # Generate 3 kamar untuk tipe kedua (type_2)
        for k in range(3):
            db.session.add(Room(
                room_id=generate_id('R'),
                room_number=k + 4,
                type_id=type_2,
                outlet_id=parsed_outlet[i]["outlet_id"],
                photo=placeholder,
                availability_status=True
            ))
            db.session.commit()

    log(here, 'Rooms Generated.')
