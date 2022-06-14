import time
import re
import os
from TP_preprocessing import clean_log_files
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def startup_cleaning():
    for root, dirs, files in os.walk(".", topdown = False):
        for file in files:
            matched = re.match("jozagv_[0-9]+\.log\.[0-9]+_[0-9]+_[0-9]+", file)
            if bool(matched):
                file_path = os.path.join(root, file)
                file_name = file
                clean_log_files(file_path, file_name)

def on_created(event):
    matched = re.match("jozagv_[0-9]+\.log\.[0-9]+_[0-9]+_[0-9]+", event.src_path[event.src_path.rfind('\\') + 1:])
    if bool(matched):
        file_name = event.src_path[event.src_path.rfind('\\') + 1:]
        file_path = event.src_path

        clean_log_files(file_path, file_name)

my_event_handler.on_created = on_created

path = "."
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive = go_recursively)
my_observer.start()
startup_cleaning()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
