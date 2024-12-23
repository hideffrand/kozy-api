from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "kozy_user"

    user_id = db.Column('user_id', db.String(10), primary_key=True)
    email = db.Column('email', db.String(150), unique=True, nullable=False)
    password = db.Column('password', db.String(100), nullable=False)
    name = db.Column('username', db.String(100), nullable=False)
    address = db.Column('address', db.String(100))
    role = db.Column('role', db.String(50))
    photo = db.Column('photo', db.String(255))
    outlet_id = db.Column('outlet_id', db.String(
        10), db.ForeignKey('kozy_outlet.outlet_id'))
    room_number = db.Column('room_number', db.Integer)

    # __mapper_args__ = {
    #     'polymorphic_on': role,
    #     'polymorphic_identity': 'user'
    # }

    def __init__(self, user_id, email, password, name, address, photo, outlet_id, room_number, role='customer'):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.name = name
        self.address = address
        self.role = role
        self.photo = photo
        self.outlet_id = outlet_id
        self.room_number = room_number

    def to_json(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "address": self.address,
            "role": self.role,
            "photo": self.photo,
            "outlet_id": self.outlet_id,
            "room_number": self.room_number,
        }


class Type(db.Model):
    __tablename__ = "kozy_type"

    type_id = db.Column('type_id', db.String(10), primary_key=True)
    type_name = db.Column('type_name', db.String(50))
    bathroom = db.Column('bathroom', db.Boolean)
    ac = db.Column('ac', db.Boolean)
    tv = db.Column('tv', db.Boolean)
    wifi_speed = db.Column('wifi_speed', db.Integer)
    mini_pantry = db.Column('mini_pantry', db.Boolean)
    dispenser = db.Column('dispenser', db.Boolean)
    fridge = db.Column('fridge', db.Boolean)
    size = db.Column('size', db.String(50))
    price = db.Column('price', db.Integer)

    def __init__(self, type_id, type_name, bathroom, ac, tv, wifi_speed, mini_pantry, dispenser, fridge, size, price):
        self.type_id = type_id
        self.type_name = type_name
        self.bathroom = bathroom
        self.ac = ac
        self.tv = tv
        self.wifi_speed = wifi_speed
        self.mini_pantry = mini_pantry
        self.dispenser = dispenser
        self.fridge = fridge
        self.size = size
        self.price = price

    def to_json(self):
        return {
            "type_id": self.type_id,
            "type_name": self.type_name,
            "bathroom": self.bathroom,
            "ac": self.ac,
            "tv": self.tv,
            "wifi_speed": self.wifi_speed,
            "mini_pantry": self.mini_pantry,
            "dispenser": self.dispenser,
            "fridge": self.fridge,
            "size": self.size,
            "price": self.price
        }


class Outlet(db.Model):
    __tablename__ = "kozy_outlet"

    outlet_id = db.Column('outlet_id', db.String(10), primary_key=True)
    name = db.Column('name', db.String(100))
    address = db.Column('address', db.String(100))
    city = db.Column('city', db.String(100))
    phone = db.Column('phone', db.String(15))
    photo = db.Column('photo', db.String(255))
    spv_id = db.Column('spv_id', db.String(10), db.ForeignKey('kozy_user.user_id'))
    motorcycle_slot = db.Column('motorcycle_slot', db.Integer)
    car_slot = db.Column('car_slot', db.Integer)

    def __init__(self, outlet_id, name, address, city, phone, photo, spv_id, motorcycle_slot, car_slot):
        self.outlet_id = outlet_id
        self.name = name
        self.address = address
        self.city = city
        self.phone = phone
        self.photo = photo
        self.spv_id = spv_id
        self.motorcycle_slot = motorcycle_slot
        self.car_slot = car_slot

    def to_json(self):
        return {
            "outlet_id": self.outlet_id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "phone": self.phone,
            "photo": self.photo,
            "spv_id": self.spv_id,
            "motorcycle_slot": self.motorcycle_slot,
            "car_slot": self.car_slot
        }


class Room(db.Model):
    __tablename__ = "kozy_room"

    room_id = db.Column('room_id', db.String(10), primary_key=True)
    room_number = db.Column('room_number', db.Integer)
    type_id = db.Column('type_id', db.String(
        10), db.ForeignKey('kozy_type.type_id'))
    outlet_id = db.Column('outlet_id', db.String(
        10), db.ForeignKey('kozy_outlet.outlet_id'))
    photo = db.Column('photo', db.String(255))
    availability_status = db.Column('availability_status', db.Boolean)

    def __init__(self, room_id, room_number, type_id, outlet_id, photo, availability_status):
        self.room_id = room_id
        self.room_number = room_number
        self.type_id = type_id
        self.outlet_id = outlet_id
        self.photo = photo
        self.availability_status = availability_status

    def to_json(self):
        return {
            "room_id": self.room_id,
            "room_number": self.room_number,
            "type_id": self.type_id,
            "outlet_id": self.outlet_id,
            "photo": self.photo,
            "availability_status": self.availability_status,
        }


class Maintenance(db.Model):
    __tablename__ = "kozy_maintenance"

    maintenance_id = db.Column(
        'maintenance_id', db.String(10), primary_key=True)
    outlet_id = db.Column('outlet_id', db.String(10),
                          db.ForeignKey('kozy_outlet.outlet_id'))
    room_number = db.Column('room_number', db.Integer)
    user_id = db.Column('user_id', db.String(
        10), db.ForeignKey('kozy_user.user_id'))
    issue = db.Column('issue', db.String(255))
    date_reported = db.Column('date_reported', db.Date)
    status = db.Column('status', db.String(50))
    resolution_date = db.Column('resolution_date', db.Date)

    def __init__(self, maintenance_id, outlet_id, room_number, user_id, issue, date_reported, status, resolution_date):
        self.maintenance_id = maintenance_id
        self.outlet_id = outlet_id
        self.room_number = room_number
        self.user_id = user_id
        self.issue = issue
        self.date_reported = date_reported
        self.status = status
        self.resolution_date = resolution_date

    def to_json(self):
        return {
            "maintenance_id": self.maintenance_id,
            "outlet_id": self.outlet_id,
            "room_number": self.room_number,
            "user_id": self.user_id,
            "issue": self.issue,
            "date_reported": self.date_reported,
            "status": self.status,
            "resolution_date": self.resolution_date
        }


class Payment(db.Model):
    __tablename__ = "kozy_payment"

    payment_id = db.Column('payment_id', db.String(10), primary_key=True)
    timestamp = db.Column('timestamp', db.Date)
    via = db.Column('via', db.String(50))
    proof = db.Column('proof', db.String(255))
    water = db.Column('water', db.Float, nullable=True)
    wifi = db.Column('wifi', db.Float, nullable=True)
    electricity = db.Column('electricity', db.Float, nullable=True)
    spv_payroll = db.Column('spv_payroll', db.Float, nullable=True)
    additional = db.Column('additional', db.Float, nullable=True)
    total = db.Column('total', db.Float)

    def __init__(self, payment_id, outlet_id, timestamp, via, proof, water, wifi, electricity, spv_payroll, additional, total):
        self.payment_id = payment_id
        self.outlet_id = outlet_id
        self.timestamp = timestamp
        self.via = via
        self.proof = proof
        self.water = water
        self.wifi = wifi
        self.electricity = electricity
        self.spv_payroll = spv_payroll
        self.additional = additional
        self.total = total

    def to_json(self):
        return {
            "payment_id": self.payment_id,
            "outlet_id": self.outlet_id,
            "timestamp": self.timestamp,
            "via": self.via,
            "proof": self.proof,
            "water": self.water,
            "wifi": self.wifi,
            "electricity": self.electricity,
            "spv_payroll": self.spv_payroll,
            "additional": self.additional,
            "total": self.total,
        }


class Booking(db.Model):
    __tablename__ = "kozy_booking"

    booking_id = db.Column('booking_id', db.String(10), primary_key=True)
    room_id = db.Column('room_id', db.String(
        10), db.ForeignKey('kozy_room.room_id'))
    outlet_id = db.Column('outlet_id', db.String(
        10), db.ForeignKey('kozy_outlet.outlet_id'))
    user_id = db.Column('user_id', db.String(
        10), db.ForeignKey('kozy_user.user_id'))
    check_in_date = db.Column('check_in_date', db.Date)
    stay_duration = db.Column('stay_duration', db.Integer)
    accepted = db.Column('accepted', db.Boolean)
    last_payment = db.Column('last_payment', db.Date)

    def __init__(self, booking_id, room_id, outlet_id, user_id, check_in_date, stay_duration, accepted, last_payment):
        self.booking_id = booking_id
        self.room_id = room_id
        self.outlet_id = outlet_id
        self.user_id = user_id
        self.check_in_date = check_in_date
        self.stay_duration = stay_duration
        self.accepted = accepted
        self.last_payment = last_payment

    def to_json(self):
        return {
            "booking_id": self.booking_id,
            "room_id": self.room_id,
            "outlet_id": self.outlet_id,
            "user_id": self.user_id,
            "check_in_date": self.check_in_date,
            "stay_duration": self.stay_duration,
            "accepted": self.accepted,
            "last_payment": self.last_payment
        }


class Transaction(db.Model):
    __tablename__ = "kozy_transaction"

    transaction_id = db.Column(
        'transaction_id', db.String(10), primary_key=True)
    user_id = db.Column('user_id', db.String(
        10), db.ForeignKey('kozy_user.user_id'))
    outlet_id = db.Column('outlet_id', db.String(
        10), db.ForeignKey('kozy_outlet.outlet_id'))
    room_id = db.Column('room_id', db.String(
        10), db.ForeignKey('kozy_room.room_id'))
    booking_id = db.Column('booking_id', db.String(
        10), db.ForeignKey('kozy_booking.booking_id'))
    cost = db.Column('cost', db.Float)
    penalty = db.Column('penalty', db.Float)
    total = db.Column('total', db.Float)
    paid_at = db.Column('paid_at', db.Date)
    due_date = db.Column('due_date', db.Date)

    def __init__(self, transaction_id, user_id, outlet_id, room_id, booking_id, cost, penalty, total, paid_at, due_date):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.outlet_id = outlet_id
        self.room_id = room_id
        self.booking_id = booking_id
        self.cost = cost
        self.penalty = penalty
        self.total = total
        self.paid_at = paid_at
        self.due_date = due_date

    def to_json(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "outlet_id": self.outlet_id,
            "room_id": self.room_id,
            "booking_id": self.booking_id,
            "cost": self.cost,
            "penalty": self.penalty,
            "total": self.total,
            "paid_at": self.paid_at,
            "due_date": self.due_date
        }
