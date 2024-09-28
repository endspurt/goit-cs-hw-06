# Базовий образ Python
FROM python:3.8-slim

# Встановлення робочої директорії
WORKDIR /app

# Копіювання файлів додатка
COPY . /app

# Встановлення необхідних пакетів
RUN pip install pymongo

# Відкриття портів для HTTP і сокет-серверів
EXPOSE 3000 5000

# Команда для запуску обох серверів
CMD ["sh", "-c", "python3 main.py & python3 socket_server.py"]
