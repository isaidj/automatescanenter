# auto_run.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class MiEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py") and event.src_path.endswith("index.py"):
            print("Detectado cambio en el código. Ejecutando automáticamente...")
            subprocess.call(["python", "index.py"])


if __name__ == "__main__":
    event_handler = MiEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
