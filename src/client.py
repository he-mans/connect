import nmap
import socket
from .settings import *


class Client():
    def __init__(self, ip: str):
        self.ip: str = ip
        self.init_socket()

    def init_socket(self):
        self.socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', CLIENT_PORT),)

    def scan_network(self, network_ip: str):
        scanner = nmap.PortScanner()
        scan = scanner.scan(
            network_ip, f'{SERVER_PORT}'
        )['scan']
        hosts = [
            (ip, stats['hostnames'][0]['name'])
            for ip, stats in scan.items() if stats['tcp'][SERVER_PORT]['state'] == 'open'
        ]
        return hosts

    def connect(self, server_ip: str):
        self.socket.connect((server_ip, SERVER_PORT),)

    def receive_file(self):
        # receiving filename
        filename = self.socket.recv(BUFFER_SIZE).decode('utf-8')
        self.socket.sendall(b'ack')

        # receiving file
        with open(f'./received/{filename}', 'wb') as f:
            complete_data = b''
            data = self.socket.recv(BUFFER_SIZE)
            while True:
                complete_data += data
                data = self.socket.recv(BUFFER_SIZE)
                if data.endswith(FINISH_HEADER):
                    self.socket.sendall(b'ack')
                    break
            f.write(complete_data)

    def listen_server_status(self):
        status: bytes = self.socket.recv(BUFFER_SIZE)
        if status.endswith(DISPOSE_HEADER):
            self.dispose()

    @property
    def is_connected(self):
        return False if self.socket.fileno() < 0 else True

    def dispose(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.dispose()
