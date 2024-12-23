from fuzzywuzzy import fuzz
from model import Outlet, db, User
from helper.logger import log
from helper.id_generator import generate_id
from service.room_service import get_outlet_rooms
import os
here = os.path.basename(__file__)


def get_all_outlets():
    log(here, "Getting outlets data...")

    outlets = Outlet.query.all()
    if not outlets:
        log(here, "Failed getting outlets data")
        return False

    return [outlet.to_json() for outlet in outlets]


def search_outlets_by_terms(search_term, threshold=80):
    log("here", "Getting outlets data...")

    outlets = Outlet.query.all()

    if not outlets:
        log("here", "Failed getting outlets data")
        return False

    matched_outlets = []

    for outlet in outlets:
        name_score = fuzz.partial_ratio(
            outlet.name.lower(), search_term.lower())
        address_score = fuzz.partial_ratio(
            outlet.address.lower(), search_term.lower())
        city_score = fuzz.partial_ratio(
            outlet.city.lower(), search_term.lower())

        if name_score > threshold or address_score > threshold or city_score > threshold:
            matched_outlets.append(outlet.to_json())

    return matched_outlets if matched_outlets else False


def get_all_outlet_cities():
    log(here, 'Getting outlet cities data...')

    outlet_cities = db.session.query(Outlet.city).distinct().all()
    if not outlet_cities:
        log(here, "Failed getting outlet cities.")

    return [city[0] for city in outlet_cities]


def get_outlet_data(id):
    log(here, "Getting outlet...")
    outlet = Outlet.query.filter_by(outlet_id=id).first()
    outlet_rooms = get_outlet_rooms(id)
    if not outlet or not outlet_rooms:
        return False

    data = outlet.to_json()
    data['rooms'] = outlet_rooms

    return data


def add_new_outlet(outlet_obj):
    log(here, "Adding new outlet...")
    if outlet_obj != {}:
        log(here, "Failed adding new outlet: Invalid data")
        return False

    new_outlet = Outlet(
        outlet_id=generate_id('O'),
        name=outlet_obj["name"],
        address=outlet_obj["address"],
        city=outlet_obj["city"],
        phone=outlet_obj["phone"],
        spv_id=outlet_obj["spv_id"],
        type_teratas=outlet_obj["type_teratas"],
        motorcycle_slot=outlet_obj["motorcycle_slot"],
        car_slot=outlet_obj["car_slot"]
    )

    db.session.add(new_outlet)
    db.session.commit()

    log(here, "New Outlet Added!")
    return True


def update_outlet(outlet_id, outlet_obj):
    log(here, "Updating outlet...")

    outlet_to_update = Outlet.query.get(outlet_id)
    if not outlet_to_update:
        log(here, f"Outlet with ID {outlet_id} not found.")
        return False

    if 'name' in outlet_obj:
        outlet_to_update.name = outlet_obj["name"]
    if 'address' in outlet_obj:
        outlet_to_update.address = outlet_obj["address"]
    if 'phone' in outlet_obj:
        outlet_to_update.phone = outlet_obj["phone"]
    if 'spv_id' in outlet_obj:
        outlet_to_update.spv_id = outlet_obj["spv_id"]
    if 'type_teratas' in outlet_obj:
        outlet_to_update.type_teratas = outlet_obj["type_teratas"]
    if 'motorcycle_slot' in outlet_obj:
        outlet_to_update.motorcycle_slot = outlet_obj["motorcycle_slot"]
    if 'car_slot' in outlet_obj:
        outlet_to_update.car_slot = outlet_obj["car_slot"]

    db.session.commit()
    log(here, f"Outlet with ID {outlet_id} updated!")
    return True


def delete_outlet(outlet_id):
    log(here, "Deleting outlet...")

    outlet_to_delete = Outlet.query.get(outlet_id)
    if not outlet_to_delete:
        log(here, f"Outlet with ID {outlet_id} not found.")
        return False

    db.session.delete(outlet_to_delete)
    db.session.commit()
    log(here, f"Outlet with ID {outlet_id} deleted!")
    return True


def generate_outlets():
    log(here, "Generating outlets...")
    spvs = db.session.query(User).filter(User.role == 'spv').all()
    parsed_spvs = [spv.to_json() for spv in spvs]
    log(here, len(parsed_spvs))

    outlet_data_jakarta = [
        {"name": "Kost Kota Jakarta", "address": "Jl. Mangga Dua Raya Blok A No. 1, RT 01 RW 02, Jakarta Pusat",
            "city": "Jakarta", "phone": "021-1234567", "spv_id": None, "type_teratas": 1, "motorcycle_slot": 10, "car_slot": 5},
        {"name": "Kost Mega City", "address": "Jl. Sudirman Kav. 50, Blok B No. 10, RT 05 RW 08, Jakarta Selatan",
            "city": "Jakarta", "phone": "021-2345678", "spv_id": None, "type_teratas": 2, "motorcycle_slot": 15, "car_slot": 8},

        {"name": "Kost Gading Indah", "address": "Jl. Gading No. 11, Blok C No. 25, RT 02 RW 04, Jakarta Utara",
            "city": "Jakarta", "phone": "021-8765432", "spv_id": None, "type_teratas": 3, "motorcycle_slot": 12, "car_slot": 6},
        {"name": "Kost Pusat Jakarta", "address": "Jl. Thamrin No. 45, Blok D No. 12, RT 03 RW 01, Jakarta Pusat",
            "city": "Jakarta", "phone": "021-9876543", "spv_id": None, "type_teratas": 4, "motorcycle_slot": 10, "car_slot": 5},
    ]
    outlet_data_bogor = [
        {"name": "Kost Bogor Indah", "address": "Jl. Raya Bogor No. 25, Blok G No. 30, RT 01 RW 02, Bogor",
            "city": "Bogor", "phone": "0251-1234567", "spv_id": None, "type_teratas": 1, "motorcycle_slot": 8, "car_slot": 4},
        {"name": "Kost Alam Sutera", "address": "Jl. Ciwaringin No. 10, Blok H No. 5, RT 02 RW 03, Bogor Barat",
            "city": "Bogor", "phone": "0251-2345678", "spv_id": None, "type_teratas": 2, "motorcycle_slot": 10, "car_slot": 5},

        {"name": "Kost Tropika", "address": "Jl. Raya Pajajaran No. 15, Blok A No. 4, RT 03 RW 05, Bogor Timur",
            "city": "Bogor", "phone": "0251-3456789", "spv_id": None, "type_teratas": 3, "motorcycle_slot": 12, "car_slot": 6},
        {"name": "Kost Warung Jati", "address": "Jl. Warung Jati No. 30, Blok B No. 10, RT 04 RW 06, Bogor",
            "city": "Bogor", "phone": "0251-8765432", "spv_id": None, "type_teratas": 4, "motorcycle_slot": 7, "car_slot": 3}
    ]
    outlet_data_depok = [
        {"name": "Kost Depok Raya", "address": "Jl. Margonda Raya No. 20, Blok D No. 5, RT 02 RW 07, Depok",
            "city": "Depok", "phone": "021-7654321", "spv_id": None, "type_teratas": 1, "motorcycle_slot": 6, "car_slot": 2},
        {"name": "Kost Margonda Suites", "address": "Jl. Margonda Raya No. 40, Blok E No. 8, RT 01 RW 04, Depok",
            "city": "Depok", "phone": "021-1234321", "spv_id": None, "type_teratas": 2, "motorcycle_slot": 9, "car_slot": 4},

        {"name": "Kost Citayam", "address": "Jl. Citayam No. 10, Blok F No. 3, RT 03 RW 02, Depok", "city": "Depok",
            "phone": "021-1122334", "spv_id": None, "type_teratas": 3, "motorcycle_slot": 10, "car_slot": 5},
        {"name": "Kost Cisalak", "address": "Jl. Cisalak No. 5, Blok G No. 2, RT 04 RW 06, Depok", "city": "Depok",
            "phone": "021-9988776", "spv_id": None, "type_teratas": 4, "motorcycle_slot": 7, "car_slot": 3}
    ]

    outlet_data_tangerang = [
        {"name": "Kost Serpong Residence", "address": "Jl. Serpong Raya No. 10, Blok H No. 7, RT 01 RW 04, Tangerang",
            "city": "Tangerang", "phone": "021-5566778", "spv_id": None, "type_teratas": 2, "motorcycle_slot": 15, "car_slot": 8},
        {"name": "Kost Tangerang City", "address": "Jl. Alamsari No. 8, Blok I No. 6, RT 02 RW 05, Tangerang Selatan",
            "city": "Tangerang", "phone": "021-6677889", "spv_id": None, "type_teratas": 3, "motorcycle_slot": 13, "car_slot": 6},

        {"name": "Kost Bintaro Jaya", "address": "Jl. Bintaro Jaya No. 22, Blok J No. 10, RT 03 RW 06, Tangerang Selatan",
            "city": "Tangerang", "phone": "021-2233445", "spv_id": None, "type_teratas": 4, "motorcycle_slot": 12, "car_slot": 5},
        {"name": "Kost BSD 2", "address": "Jl. Raya BSD No. 33, Blok K No. 15, RT 04 RW 02, Tangerang", "city": "Tangerang",
            "phone": "021-9988775", "spv_id": None, "type_teratas": 1, "motorcycle_slot": 6, "car_slot": 3}
    ]
    outlet_data_bekasi = [
        {"name": "Kost Bekasi Baru", "address": "Jl. Raya Bekasi No. 5, Blok L No. 12, RT 01 RW 03, Bekasi",
            "city": "Bekasi", "phone": "021-3344556", "spv_id": None, "type_teratas": 2, "motorcycle_slot": 10, "car_slot": 5},
        {"name": "Kost Grand Bekasi", "address": "Jl. Bekasi Timur No. 30, Blok M No. 7, RT 02 RW 05, Bekasi",
            "city": "Bekasi", "phone": "021-2233447", "spv_id": None, "type_teratas": 3, "motorcycle_slot": 12, "car_slot": 6},

        {"name": "Kost Indah Permai", "address": "Jl. Perumahan Indah No. 50, Blok N No. 3, RT 04 RW 07, Bekasi",
            "city": "Bekasi", "phone": "021-4455669", "spv_id": None, "type_teratas": 1, "motorcycle_slot": 8, "car_slot": 4},
        {"name": "Kost Bekasi Sentral", "address": "Jl. Raya Bekasi Timur No. 55, Blok O No. 9, RT 01 RW 02, Bekasi",
            "city": "Bekasi", "phone": "021-8899001", "spv_id": None, "type_teratas": 4, "motorcycle_slot": 14, "car_slot": 7}
    ]

    all_outlets = outlet_data_jakarta + outlet_data_bogor + \
        outlet_data_depok + outlet_data_tangerang + outlet_data_bekasi
    for i, outlet_obj in enumerate(all_outlets):
        oid = generate_id('O')
        new_outlet = Outlet(
            outlet_id=oid,
            name=outlet_obj["name"],
            address=outlet_obj["address"],
            city=outlet_obj["city"],
            phone=outlet_obj["phone"],
            photo=None,
            spv_id=parsed_spvs[i]["user_id"],
            motorcycle_slot=outlet_obj["motorcycle_slot"],
            car_slot=outlet_obj["car_slot"]
        )
        db.session.add(new_outlet)
        user = User.query.filter_by(user_id=parsed_spvs[i]["user_id"]).first()
        if user:
            user.outlet_id = oid
        db.session.commit()

    log(here, "Outlets generated.")
