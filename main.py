import http.server
import socketserver
import socket
import json
import datetime
from urllib.parse import urlparse, parse_qs

PORT = 3000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    # Обробка GET-запитів
    def do_GET(self):
        # Визначення маршруту для головної сторінки
        if self.path == "/":
            self.path = "front-init/index.html"
        # Визначення маршруту для сторінки з повідомленням
        elif self.path == "/message":
            self.path = "front-init/message.html"
        # Визначення маршруту для статичних ресурсів (CSS та логотип)
        elif self.path == "/style.css":
            self.path = "front-init/style.css"
        elif self.path == "/logo.png":
            self.path = "front-init/logo.png"
        # Визначення маршруту для сторінки з помилкою
        else:
            self.path = "front-init/error.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Обробка POST-запитів (відправка даних з форми)
    def do_POST(self):
        if self.path == "/submit_message":
            # Отримання даних з форми
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))

            # Форматування даних для відправки на сервер сокетів
            message_data = {
                "date": str(datetime.datetime.now()),
                "username": data['username'][0],
                "message": data['message'][0]
            }

            # Відправка даних на сокет-сервер через UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(json.dumps(message_data).encode('utf-8'), ('localhost', 5000))

            # Відповідь клієнту після успішного відправлення
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Message submitted successfully!")

# Запуск HTTP сервера
handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", PORT), handler_object)

print(f"HTTP сервер працює на порту {PORT}")
my_server.serve_forever()
