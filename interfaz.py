import tkinter
from tkinter import ttk
import qrcode
import socket
from PIL import ImageTk, Image
import sv_ttk


def obtener_ip():
    try:
        # Obtener el nombre del host
        host_name = socket.gethostname()

        # Obtener la dirección IP del host
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except Exception as e:
        print("Error al obtener la dirección IP:", e)
        return None


def generar_qr():
    ip = obtener_ip()
    if ip:
        qr = qrcode.make(ip)
        qr_img = ImageTk.PhotoImage(qr)
        qr_label.config(image=qr_img)
        qr_label.image = qr_img
    else:
        qr_label.config(text="Error al obtener la IP", image=None)


# Crear la ventana principal
root = tkinter.Tk()
root.title("Generador de Código QR de IP")
# position centered window
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))
# abre ventana importante
root.attributes("-topmost", True)

# Obtener la IP local
ip_label = ttk.Label(
    root,
    text="Escanea el código QR en tu dispositivo móvil",
    font=("Arial", 12, "bold"),
)
ip_label.pack(pady=10, padx=50)
ip = obtener_ip()
ip_value_label = ttk.Label(root, text=ip)
ip_value_label.pack(pady=5)

# Generar el código QR de la IP
qr = qrcode.make(ip)
qr_img = ImageTk.PhotoImage(qr)

# Etiqueta para mostrar el código QR generado
qr_label = ttk.Label(root, image=qr_img)
qr_label.pack()

# Botón para actualizar el código QR de la IP
generate_button = ttk.Button(root, text="Actualizar QR de IP", command=generar_qr)
generate_button.pack(pady=10)

sv_ttk.set_theme("light")
# Ejecutar el bucle principal de la interfaz
root.mainloop()
