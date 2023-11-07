import re
import uuid


def generate_id(value, postfix=str):
    pattern = r"[^a-zA-Z0-9 ]"
    if not value:
        unique_id = uuid.uuid4()
        prefix = str(unique_id)[:6]
        value = f"{prefix}_" + re.sub(pattern, "", postfix.lower())
    return re.sub(r"\s+", " ", value).replace(" ", "_")


def generate_token(value):
    if not value:
        generate = uuid.uuid4()
        value = str(generate)[:6]
    return value
