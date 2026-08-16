import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_user():
    return {
        "email": f"{random_string()}@mail.com",
        "password": "123456",
        "name": f"User_{random_string(5)}"
    }