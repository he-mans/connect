from time import sleep
from enum import Enum
from typing import Any
import threading
import socket
import os
from progress.spinner import Spinner


class Action(str, Enum):
    SEND: str = 'Send'
    RECEIVE: str = 'Receive'


class FollowUpAction(str, Enum):
    SEND_ANOTHER: str = 'Send Another'
    RETURN_HOME: str = 'Return Hone'


class SpinnerThread(threading.Thread):

    def __init__(self, spinner: Spinner,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spinner: Spinner = spinner
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            sleep(.1)
            self.spinner.next()


def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def get_filename(path: str) -> str:
    return os.path.basename(path)
