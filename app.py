import tkinter as tk
from tkinter import ttk
import qrcode
import socket
from PIL import Image, ImageTk

import threading
import socketServer


class QRCodeGeneratorApp:
    def __init__(self, root):
        # Inicializar la ventana principal
        self.root = root
        self.root.title("Generador de Código QR de IP")
        self.root.geometry("+300+150")
        self.root.attributes("-topmost", True)

        # Crear etiquetas y botón en la interfaz
        self.ip_label = ttk.Label(
            self.root,
            text="Escanea el código QR en tu dispositivo móvil",
            font=("Arial", 12, "bold"),
        )
        self.ip_label.pack(pady=10, padx=50)

        self.ip_value_label = ttk.Label(self.root, text="")
        self.ip_value_label.pack(pady=5)

        self.empty_qr_img = ImageTk.PhotoImage(Image.new("RGB", (1, 1), color="white"))
        self.qr_label = ttk.Label(self.root, image=self.empty_qr_img)
        self.qr_label.pack()

        self.generate_button = ttk.Button(
            self.root, text="Actualizar QR de IP", command=self.generar_qr
        )
        self.generate_button.pack(pady=10)

        # Iniciar el servidor en un hilo
        self.server_thread = threading.Thread(target=socketServer.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        # Ejecutar la función comprobar_ip al inicio
        self.comprobar_ip()

    def obtener_ip(self):
        # Función para obtener la dirección IP local del dispositivo
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address

        except Exception as e:
            print("Error al obtener la dirección IP:", e)
            return None

    def generar_qr(self):
        # Función para generar el código QR y mostrarlo en la interfaz
        ip = self.obtener_ip()
        if ip is not None:
            qr = qrcode.make(ip)
            qr_img = ImageTk.PhotoImage(qr)
            self.qr_label.config(image=qr_img)
            self.qr_label.image = qr_img
            self.ip_value_label.config(text=ip)
        else:
            self.qr_label.config(image=self.empty_qr_img)
            self.qr_label.image = self.empty_qr_img
            self.ip_value_label.config(text="Conéctate a la red")

    def comprobar_ip(self):
        # Función para comprobar la IP y actualizar el código QR periódicamente
        ip = self.obtener_ip()
        if ip is not None:
            self.generar_qr()
            delay = 5000  # 5 segundos (en milisegundos)
        else:
            self.qr_label.config(image=self.empty_qr_img)
            self.qr_label.image = self.empty_qr_img
            self.ip_value_label.config(text="Conéctate a la red")
            delay = 1000  # 1 segundo (en milisegundos)

        # Ejecutar nuevamente la función comprobar_ip después del retraso
        self.root.after(delay, self.comprobar_ip)


# Crear la ventana principal y la instancia de la clase QRCodeGeneratorApp
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
