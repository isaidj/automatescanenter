import socketio
import time
import pyautogui
import pyperclip
import json
import threading
import socket

# Crear una instancia de socket.io cliente
sio = socketio.Client()

# Variables para el descubrimiento de servicios
SERVER_DISCOVERY_PORT = 5000
SERVER_DISCOVERY_MESSAGE = "HelloServer"
server_ip = None


# Función para el descubrimiento de servicios
def discover_server():
    global server_ip
    # Crear un socket UDP para recibir mensajes de difusión
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_socket.bind(("", SERVER_DISCOVERY_PORT))

    while True:
        data, addr = discovery_socket.recvfrom(1024)
        if data.decode() == SERVER_DISCOVERY_MESSAGE:
            # Cuando se recibe el mensaje de descubrimiento, almacenar la dirección IP del servidor
            server_ip = addr[0]
            break


# Iniciar el hilo para descubrir el servidor
discovery_thread = threading.Thread(target=discover_server)
discovery_thread.daemon = True
discovery_thread.start()


# Función para ejecutar comandos de teclado
def ejecutar_comandos_teclado(data):
    pyautogui.sleep(0)
    # Copia al portapapeles data
    pyperclip.copy(data)
    # Simula presionar las teclas "control + v"
    pyautogui.hotkey("ctrl", "v")
    # Simula presionar la tecla "enter"
    pyautogui.press("enter")


# Define la función que se ejecutará cuando se establezca la conexión con el servidor
@sio.on("connect", namespace="/")
def on_connect():
    print("Conectado al servidor")


# Define la función que se ejecutará cuando se cierre la conexión con el servidor
@sio.on("disconnect", namespace="/")
def on_disconnect():
    print("Desconectado del servidor")


# Define la función que se ejecutará cuando se dispare el evento "recive_scan" desde el servidor
@sio.on("recive_scan", namespace="/")
def on_recive_scan(data):
    print("Evento 'recive_scan' ")
    value = data["data"]
    print(value)

    ejecutar_comandos_teclado(value)


# Esperar hasta que se descubra la dirección IP del servidor
while not server_ip:
    time.sleep(1)

# Conectar al servidor de socket.io utilizando la dirección IP descubierta
sio.connect(f"http://{server_ip}:3002")

# Verificar si el cliente está conectado
if sio.connected:
    print("Cliente conectado al servidor" + server_ip)
else:
    print("Cliente NO conectado al servidor.")

# Mantener el cliente en ejecución
sio.wait()
