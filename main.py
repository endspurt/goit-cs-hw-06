import http.server
import socketserver
import socket
import json
import datetime
import os  # Для роботи з файловою системою
from urllib.parse import parse_qs

# Порт для HTTP-сервера
PORT = 3000
# Шлях до директорії з файлами "storage"
STORAGE_PATH = 'front-init/storage'

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    # Обробка GET-запитів (запит сторінок або файлів)
    def do_GET(self):
        # Визначення маршрутів для різних сторінок
        if self.path == "/":
            self.path = "front-init/index.html"
        elif self.path == "/message":
            self.path = "front-init/message.html"
        elif self.path == "/style.css":
            self.path = "front-init/style.css"
        elif self.path == "/logo.png":
            self.path = "front-init/logo.png"
        # Обробка файлів з директорії "storage"
        elif self.path.startswith("/storage/"):
            # Створення шляху до файлу в "storage"
            file_path = os.path.join(STORAGE_PATH, self.path.lstrip("/storage/"))
            if os.path.exists(file_path):
                # Якщо файл існує, то обробляємо його
                self.path = file_path
            else:
                # Якщо файл не знайдений, показуємо сторінку з помилкою
                self.path = "front-init/error.html"
        else:
            # Якщо маршрут не відповідає жодній з наявних сторінок, повертаємо сторінку з помилкою
            self.path = "front-init/error.html"
        
        # Виклик методу для обробки GET-запиту
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Обробка POST-запитів (обробка форм)
    def do_POST(self):
        if self.path == "/submit_message":
            # Отримуємо дані форми
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))

            # Створюємо словник з повідомленням
            message_data = {
                "date": str(datetime.datetime.now()),
                "username": data['username'][0],
                "message": data['message'][0]
            }

            # Відправляємо дані на сокет-сервер через UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(json.dumps(message_data).encode('utf-8'), ('localhost', 5000))

            # Повертаємо відповідь клієнту після успішного надсилання
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Message submitted successfully!")

# Старт HTTP-сервера
handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", PORT), handler_object)

print(f"HTTP-сервер працює на порту {PORT}")
my_server.serve_forever()
