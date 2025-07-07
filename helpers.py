import random
import string

def generate_random_string(length=8):
    """Генерирует случайную строку из букв."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def get_sample_order_data():
    """Возвращает шаблон данных заказа."""
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
