import secrets
import string


def generate_random_string(length: int = secrets.randbelow(98) + 3) -> str:
    characters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join(secrets.choice(characters) for _ in range(length))
