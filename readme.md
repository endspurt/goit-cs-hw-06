### Schrittweise Erklärung

1. **HTTP-Server (main.py)**
   - **GET-Anfragen**: Der HTTP-Server wird mit dem `http.server`-Modul in Python erstellt. Jede GET-Anfrage wird abhängig von der Route (`/`, `/message`, `/style.css`, usw.) an die entsprechenden Dateien weitergeleitet, die statische HTML, CSS und Bilddateien sind.
   - **POST-Anfragen**: Wenn der Benutzer das Formular auf der `message.html`-Seite ausfüllt und abschickt, wird eine POST-Anfrage an den Server gesendet. Die Daten (Benutzername und Nachricht) werden extrahiert und an den Socket-Server gesendet, der auf Port 5000 läuft.

2. **Socket-Server (socket_server.py)**
   - Der Socket-Server wird auf Port 5000 gestartet und wartet auf eingehende UDP-Pakete, die Nachrichten enthalten.
   - Wenn eine Nachricht empfangen wird, wird sie in eine Python-Datenstruktur (Wörterbuch) konvertiert und in der MongoDB-Datenbank gespeichert.
   - MongoDB wird in einem separaten Docker-Container ausgeführt, der über die Docker-Compose-Datei eingerichtet wird.

3. **Docker-Konfiguration**
   - **Dockerfile** Dieser definiert, wie die Webanwendung und der Socket-Server in einem Docker-Container ausgeführt werden. Die erforderlichen Python-Pakete werden installiert, und die Server laufen parallel, um HTTP- und Socket-Anfragen zu bedienen.
   - **docker-compose.yaml**: Docker Compose orchestriert mehrere Container, darunter die Webanwendung und die MongoDB. Die Datenbank wird in einem persistenten Volume gespeichert, sodass Daten auch nach dem Neustart des Containers erhalten bleiben.

4. **Verzeichnisstruktur**
   - Die HTML-Dateien, CSS und das Bildlogo befinden sich im Ordner `front-init`, der als Quelle für die statischen Dateien dient.
   - Das Python-Programm (`main.py`) und der Socket-Server (`socket_server.py`) greifen auf diese Dateien zu und bedienen sie über den HTTP-Server.

### Ausführung der Lösung

1. **Docker-Container erstellen und starten**
   - Um die Anwendung zu starten, führe in deinem Projektordner folgenden Befehl aus
     
     docker-compose up --build
     ```
    Dies erstellt und startet sowohl den HTTP-Server als auch den Socket-Server in Docker-Containern, wobei MongoDB ebenfalls bereitgestellt wird.

2. **Zugriff auf die Anwendung**
   - Öffne `http://localhost:3000` in deinem Browser, um auf die Hauptseite der Anwendung zuzugreifen.
   - Auf der Seite `message.html` kannst du eine Nachricht eingeben, die dann über den Socket-Server in der MongoDB gespeichert wird.

