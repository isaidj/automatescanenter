import eventlet
import socketio

# Crear una instancia de socket.io servidor
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)


# Evento que se ejecuta cuando un cliente se conecta al servidor
@sio.event
def connect(sid, environ):
    print(f"Cliente conectado: {sid}")


# Evento que se ejecuta cuando un cliente se desconecta del servidor
@sio.event
def disconnect(sid):
    print(f"Cliente desconectado: {sid}")


# Evento personalizado que se ejecuta cuando el servidor recibe el evento "scan"
@sio.event
def scan(sid, data):
    print(f"Evento 'scan' recibido con datos: {data}")
    # Realiza cualquier lógica que desees con los datos recibidos


# Ejecutar el servidor socket.io en el puerto 3002
if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 3002)), app)
