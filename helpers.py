# helpers.py
import random
import string

def generate_random_string(length=10) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_courier_data() -> dict:
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }

def generate_order_data() -> dict:
    return {
        'firstName': 'Ivan',
        'lastName': 'Ivanov',
        'address': 'Lenina street',
        'metroStation': '4',
        'phone': '+79991112233',
        'rentTime': 5,
        'deliveryDate': '2023-10-10',
        'comment': '',
        'color': [], 
        'price': 1000,
    }
