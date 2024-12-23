import uuid


def generate_id(prefix):
    random_uuid = uuid.uuid4().hex[:7]
    result = f"{prefix}{random_uuid}".upper()

    return result
