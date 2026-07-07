import string
import random

BASE62_CHARS = string.ascii_letters + string.digits

def generate_short_slug(length: int = 7) -> str:
    return ''.join(
        random.choices(BASE62_CHARS, k=length)
    )