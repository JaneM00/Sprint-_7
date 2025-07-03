# helpers.py

from urls import BASE_URL

def get_full_url(endpoint):
    return f"{BASE_URL}{endpoint}"

def create_courier_payload(login="testuser", password="testpass"):
    return {
        "login": login,
        "password": password
    }

def create_order_payload():
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
