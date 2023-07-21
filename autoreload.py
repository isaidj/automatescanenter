import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen


class HotReloader(FileSystemEventHandler):
    def __init__(self, target_file):
        self.target_file = target_file
        self.process = None

    def on_any_event(self, event):
        if event.src_path.endswith(self.target_file):
            self.restart_process()

    def restart_process(self):
        print("Reloading...")
        if self.process:
            self.process.terminate()
        self.process = Popen(["python3", self.target_file])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hot_reload.py your_file.py")
    else:
        target_file = sys.argv[1]
        event_handler = HotReloader(target_file)
        observer = Observer()
        observer.schedule(event_handler, path=".", recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
