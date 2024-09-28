import socket
import json
from pymongo import MongoClient

# Налаштування MongoDB
client = MongoClient('mongodb://mongo:27017/')
db = client['message_database']
collection = db['messages']

# Функція для запуску сокет-сервера
def start_socket_server():
    # Налаштування UDP сокет-сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))
    print("Сокет-сервер працює на порту 5000")

    # Бездротовий цикл для отримання повідомлень
    while True:
        data, addr = server_socket.recvfrom(1024)
        message_data = json.loads(data.decode('utf-8'))
        print(f"Отримані дані: {message_data}")

        # Збереження даних у MongoDB
        collection.insert_one(message_data)

if __name__ == "__main__":
    start_socket_server()
