import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, app_process):
        self.app_process = app_process

    def on_any_event(self, event):
        if event.is_directory:
            return

        if event.event_type in ['modified', 'created']:
            print("Reloading application...")
            self.app_process.terminate()
            self.app_process.wait()

            # Restart the application
            new_app_process = subprocess.Popen(["python", "-m", "src.main"])
            self.app_process = new_app_process

if __name__ == "__main__":
    app_process = subprocess.Popen(["python", "-m", "src.main"])
    
    event_handler = MyHandler(app_process)
    observer = Observer()
    observer.schedule(event_handler, path="./", recursive=False)  # Monitor the current directory, change path as needed
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
