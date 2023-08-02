import socket
import pyautogui
import pyperclip
import threading
from flask import Flask, request

app = Flask(__name__)

server_port = 5000


def obtener_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print("Nombre del host:", socket.gethostname())
        ip_address = s.getsockname()[0]
        s.close()
        host_info = {"hostname": socket.gethostname(), "ip": ip_address}
        return host_info
    except Exception as e:
        print("Error al obtener la dirección IP:", e)
        return None


# Función para copiar al portapapeles de manera asíncrona
def copy_clipboard_async(text):
    def copy_task():
        pyperclip.copy(text)
        # Detecta si está en Windows o Mac
        if pyautogui.os.name == "nt":
            # Simula presionar las teclas "control + v"
            pyautogui.hotkey("ctrl", "v")
        else:
            # Simula presionar las teclas "command + v"
            pyautogui.hotkey("command", "v")
        pyautogui.sleep(0.2)
        pyautogui.press("enter")

    # Ejecuta la función en un hilo separado
    thread = threading.Thread(target=copy_task)
    thread.start()


# Ruta para manejar la solicitud POST del evento "scan"
@app.route("/scan", methods=["POST"])
def scan():
    try:
        data = request.json
        print("Evento 'scan' recibido con datos:", data)
        # Realiza cualquier lógica que desees con los datos recibidos
        # {'data': '9789588715513'}
        print(data)
        print(data["data"])
        # Copia al portapapeles el código de barras de forma asíncrona

        # remplace "-" for "'"
        new_data = data["data"].replace("-", "'")
        copy_clipboard_async(new_data)
        return "Operación exitosa", 200
    except Exception as e:
        return f"Error: {e}", 500


@app.route("/status", methods=["GET"])
def status():
    try:
        print("Conectado a " + obtener_ip().get("hostname"))
        # Realiza cualquier lógica que desees con los datos recibidos
        return obtener_ip(), 200
    except Exception as e:
        return f"Error: {e}", 500


def run_server():
    # Ejecutar el servidor en el puerto 5000
    ip = obtener_ip().get("ip")

    if ip is not None:
        app.run(host=ip, port=server_port)
        print(f"Iniciando servidor en http://{ip}:{server_port}")
    else:
        print("No se pudo obtener la dirección IP para iniciar el servidor.")


if __name__ == "__main__":
    run_server()
