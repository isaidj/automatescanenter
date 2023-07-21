import tkinter
from tkinter import ttk
import qrcode
import socket
from PIL import Image, ImageTk
import threading
import socketServer


def obtener_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        # print("Dirección IP:", ip_address)
        return ip_address

    except Exception as e:
        print("Error al obtener la dirección IP:", e)
        return None


def generar_qr():
    ip = obtener_ip()
    if ip is not None:
        qr = qrcode.make(ip)
        qr_img = ImageTk.PhotoImage(qr)
        qr_label.config(image=qr_img)
        qr_label.image = qr_img
        ip_value_label.config(text=ip)
    else:
        qr_label.config(image=empty_qr_img)
        qr_label.image = empty_qr_img
        ip_value_label.config(text="Conéctate a la red")


def comprobar_ip():
    ip = obtener_ip()
    if ip is not None:
        generar_qr()
        delay = 5000  # 5 seconds (in milliseconds)
    else:
        qr_label.config(image=empty_qr_img)
        qr_label.image = empty_qr_img
        ip_value_label.config(text="Conéctate a la red")

        delay = 1000  # 1 second (in milliseconds)

    root.after(delay, comprobar_ip)


# Create the main window
root = tkinter.Tk()
root.title("Generador de Código QR de IP")

# Position centered window
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 1.3 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 4 - windowHeight / 2)
root.geometry("+{}+{}".format(positionRight, positionDown))
root.attributes("-topmost", True)

# Get the local IP and generate the QR code at startup
ip_label = ttk.Label(
    root,
    text="Escanea el código QR en tu dispositivo móvil",
    font=("Arial", 12, "bold"),
)
ip_label.pack(pady=10, padx=50)

ip_value_label = ttk.Label(root, text="")
ip_value_label.pack(pady=5)

empty_qr_img = ImageTk.PhotoImage(Image.new("RGB", (1, 1), color="white"))
qr_label = ttk.Label(root, image=empty_qr_img)
qr_label.pack()

generate_button = ttk.Button(root, text="Actualizar QR de IP", command=generar_qr)
generate_button.pack(pady=10)

server_thread = threading.Thread(target=socketServer.run_server)
server_thread.daemon = True
server_thread.start()

# Run the comprobar_ip function in the background to detect network connection automatically
thread = threading.Thread(target=comprobar_ip)
thread.daemon = True
thread.start()

# Execute the main loop of the interface
root.mainloop()
