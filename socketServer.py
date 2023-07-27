import os

os.environ["EVENTLET_HUB"] = "LIBEVENT_NOPOLL"

import eventlet
import socketio
import socket
import pyautogui
import pyperclip


def obtener_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address

    except Exception as e:
        print("Error al obtener la dirección IP:", e)
        return None


# copiar al portapapeles
def copy_clipboard(text):
    pyperclip.copy(text)
    # detecta si esta en windows o o mac
    if pyautogui.os.name == "nt":
        # Simula presionar las teclas "control + v"
        pyautogui.hotkey("ctrl", "v")
    else:
        # Simula presionar las teclas "command + v"
        pyautogui.hotkey("command", "v")

    pyautogui.sleep(1.5)
    pyautogui.press("enter")


# Crear una instancia de socket.io servidor
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)


# Evento que se ejecuta cuando un cliente se conecta al servidor
@sio.event
def connect(sid, environ):
    print("Cliente conectado")


# Evento que se ejecuta cuando un cliente se desconecta del servidor
@sio.event
def disconnect(sid):
    print("Cliente desconectado")


# Evento personalizado que se ejecuta cuando el servidor recibe el evento "scan"
@sio.event
def scan(sid, data):
    print("Evento 'scan' recibido con datos: {data}")
    # Realiza cualquier lógica que desees con los datos recibidos
    # {'data': '9789588715513'}
    print(data)
    print(data["data"])
    # Copia al portapapeles el código de barras
    copy_clipboard(data["data"])


def run_server():
    # Ejecutar el servidor socket.io en el puerto 3002
    ip = obtener_ip()
    if ip is not None:
        print("Iniciando servidor en http://{ip}:3002")
        eventlet.wsgi.server(eventlet.listen((ip, 3002)), app)
    else:
        print("No se pudo obtener la dirección IP para iniciar el servidor.")


if __name__ == "__main__":
    run_server()
