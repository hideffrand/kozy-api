from model import User, db
from helper.id_generator import generate_id
from helper.logger import log
from service.auth_service import hash_password
import os
import bcrypt
here = os.path.basename(__file__)


def register(user_obj):
    log(here, f"Registering user {user_obj['email']}...")

    # Hash the password before saving to the database
    hashed_password = hash_password(user_obj["password"])

    # Create the user record with the hashed password
    new_user = User(
        user_id=generate_id('U'),
        email=user_obj["email"],
        password=hashed_password,  # Store the hashed password
        name=user_obj["name"],
        address=user_obj["address"],
        role='customer',
        photo=None,
        outlet_id=None,
        room_number=None,
    )

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    log(here, "New User Created!")

    # Fetch the user to return the JSON representation
    user = User.query.filter_by(email=user_obj['email']).first()
    if not user:
        return False

    return user.to_json()


def update_user(user_id, user_obj):
    log(here, "Updating user...")

    if not user_obj or not isinstance(user_obj, dict):
        log(here, "Invalid user object. Failed updating user.")
        return False

    try:
        # Find the user by ID
        user_to_update = User.query.get(user_id)
        if not user_to_update:
            log(here, f"user with ID {user_id} not found.")
            return False

        # Update user attributes dynamically
        for key, value in user_obj.items():
            if hasattr(user_to_update, key):
                setattr(user_to_update, key, value)

        # Commit the changes
        db.session.commit()
        log(here, f"user with ID {user_id} updated successfully!")
        return True
    except Exception as e:
        log(here, f"Error updating user: {e}")
        return False


def login(user_obj):
    try:
        log(here, f"User {user_obj['email']} logging in...")

        user = User.query.filter_by(email=user_obj['email']).first()

        if not user:
            log(here, "Login Failed: User not found")
            return False

        if not bcrypt.checkpw(user_obj['password'].encode('utf-8'), user.password.encode('utf-8')):
            log(here, "Login Failed: Incorrect password")
            return False

        log(here, "Login Success")
        return user.to_json()

    except Exception as e:
        log(here, f"Error login {user_obj['email']}: {e}")
        return False


def get_user_data(id):
    log(here, "Getting user data...")
    user = User.query.filter_by(user_id=id).first()
    if not user:
        log(here, "Failed getting user data")
        return False

    return user.to_json()


def get_all_users(role):
    log(here, "Getting all user...")
    if role:
        users = User.query.filter_by(role=role).all()
    else:
        users = User.query.all()

    if not users:
        log(here, "Failed getting user data")
        return False

    return [user.to_json() for user in users]


def get_user_data_by_email(email):
    log(here, "Getting user data...")
    user = User.query.filter_by(email=email).first()
    if not user:
        log(here, "Failed getting user data by email")
        return False

    return user.to_json()


def get_user_role(user_obj):
    return user_obj['role']


def generate_spvs():
    log(here, 'Generating SPVs...')
    spvs = [
        User(
            user_id=generate_id('U'),
            email="customer@gmail.com",
            password=hash_password("customer123"),
            name="customer",
            address="BLOK",
            role="customer",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="owner@gmail.com",
            password=hash_password("owner123"),
            name="owner",
            address="BLOK",
            role="owner",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="rudisantoso@gmail.com",
            password=hash_password("Rudi123"),
            name="Rudi Santoso",
            address="Jl. Merdeka No. 12, RT 01 RW 03, Jakarta",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="dinapratiwi@gmail.com",
            password=hash_password("Dina123"),
            name="Dina Pratiwi",
            address="Jl. Sudirman No. 34, RT 02 RW 01, Surabaya",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="budisetiawan@gmail.com",
            password=hash_password("Budi123"),
            name="Budi Setiawan",
            address="Jl. Raya No. 56, RT 05 RW 02, Bandung",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="sitiaminah@gmail.com",
            password=hash_password("Siti123"),
            name="Siti Aminah",
            address="Jl. Panglima Polim No. 78, RT 03 RW 04, Medan",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="andihidayat@gmail.com",
            password=hash_password("Andi123"),
            name="Andi Hidayat",
            address="Jl. Dago No. 90, RT 02 RW 05, Semarang",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="nurulaisyah@gmail.com",
            password=hash_password("Nurul123"),
            name="Nurul Aisyah",
            address="Jl. Gajah Mada No. 12, RT 01 RW 06, Makassar",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="agusrahman@gmail.com",
            password=hash_password("Agus123"),
            name="Agus Rahman",
            address="Jl. Pahlawan No. 43, RT 04 RW 07, Yogyakarta",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="linamarlina@gmail.com",
            password=hash_password("Lina123"),
            name="Lina Marlina",
            address="Jl. Satrio No. 21, RT 02 RW 08, Palembang",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="rizkyakbar@gmail.com",
            password=hash_password("Rizky123"),
            name="Rizky Akbar",
            address="Jl. Abdul Muis No. 100, RT 01 RW 09, Bali",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="mayaputri@gmail.com",
            password=hash_password("Maya123"),
            name="Maya Putri",
            address="Jl. Cihampelas No. 45, RT 03 RW 01, Malang",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="farhanazis@gmail.com",
            password=hash_password("Farhan123"),
            name="Farhan Azis",
            address="Jl. Setiabudi No. 12, RT 02 RW 02, Tangerang",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="dewianggraini@gmail.com",
            password=hash_password("Dewi123"),
            name="Dewi Anggraini",
            address="Jl. Ahmad Yani No. 67, RT 04 RW 03, Bekasi",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="ekoprasetyo@gmail.com",
            password=hash_password("Eko123"),
            name="Eko Prasetyo",
            address="Jl. Pahlawan Revolusi No. 33, RT 01 RW 04, Bogor",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="titihandayani@gmail.com",
            password=hash_password("Titi123"),
            name="Titi Handayani",
            address="Jl. Tendean No. 88, RT 05 RW 05, Depok",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="mochamadiqbal@gmail.com",
            password=hash_password("Mochamad123"),
            name="Mochamad Iqbal",
            address="Jl. Kebon Jeruk No. 20, RT 02 RW 06, Samarinda",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="yuliaputri@gmail.com",
            password=hash_password("Yulia123"),
            name="Yulia Putri",
            address="Jl. Pasir Kaliki No. 10, RT 01 RW 07, Pontianak",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="zainalarifin@gmail.com",
            password=hash_password("Zainal123"),
            name="Zainal Arifin",
            address="Jl. Soekarno Hatta No. 66, RT 03 RW 08, Manado",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="tasyaamalia@gmail.com",
            password=hash_password("Tasya123"),
            name="Tasya Amalia",
            address="Jl. Veteran No. 43, RT 04 RW 09, Bandar Lampung",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="iwankurniawan@gmail.com",
            password=hash_password("Iwan123"),
            name="Iwan Kurniawan",
            address="Jl. Alun-Alun No. 15, RT 02 RW 10, Cirebon",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        ),
        User(
            user_id=generate_id('U'),
            email="nadiasari@gmail.com",
            password="Nadia123",
            name=hash_password("Nadia Sari"),
            address="Jl. Merdeka No. 78, RT 01 RW 11, Jakarta",
            role="spv",
            photo=None,
            outlet_id=None,
            room_number=None,
        )
    ]

    for spv in spvs:
        db.session.add(spv)
        db.session.commit()

    log(here, "SPVs generated.")
