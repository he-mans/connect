import socket
from typing import Tuple
from time import sleep
import os
from .utils import get_filename
from .settings import *
from .ui import UI


class Server():
    def __init__(self, ip: str):
        self.conn: socket.socket = None
        self.conn_addr: str = None
        self.ip: str = ip
        self.init_socket()

    def init_socket(self):
        self.socket: socket.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, SERVER_PORT),)
        self.socket.listen(1)

    def connect_to_client(self):
        conn: socket.socket
        addr: Tuple[str]
        conn, addr = self.socket.accept()
        if addr[-1] != CLIENT_PORT:
            return None
        self.conn = conn
        self.conn_addr = addr[0]

    def transfer_file(self, filepath: str):
        # sending filename
        filename = get_filename(filepath)
        self.conn.sendall(filename.encode())
        self.conn.recv(BUFFER_SIZE)

        # sending file size
        filesize: int = os.stat(filepath).st_size
        self.conn.sendall(str(filesize).encode())
        self.conn.recv(BUFFER_SIZE)

        progress = UI.progress_bar("Sending file", filesize)
        progress.next()

        # sending file
        with open(filepath, 'rb') as f:
            data = f.read(BUFFER_SIZE)
            while data:
                sleep(1)
                self.conn.sendall(data)
                progress.next(len(data))
                data = f.read(BUFFER_SIZE)
            progress.finish()
            self.conn.sendall(FINISH_HEADER)
            self.conn.recv(BUFFER_SIZE)

    def notify_client(self, cont=True, dispose=False):
        if dispose:
            self.conn.sendall(DISPOSE_HEADER)
        else:
            self.conn.sendall(CONTINUE_HEADER)

    def dispose(self):
        self.conn.close()
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.dispose()

    @property
    def is_connected(self):
        return False if self.conn == None else True
