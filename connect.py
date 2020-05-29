import nmap
import socket
from ui import UI
from utils import *
from server import Server
from client import Client


class Connect:
    def __init__(self):
        self.ip: str = get_ip_address()
        self.network_ip: str = f'{self.ip}/24'

    def start(self):
        while True:
            action = UI.prompt_action()
            self.init_server() if action == Action.SEND else self.init_client()

    def init_server(self):
        with Server(self.ip) as server:
            while True:
                spinner = UI.get_spinner('Waiting for receiver to connect ')
                while not server.is_connected:
                    server.connect_to_client()
                UI.stop_spinner(spinner)
                print(f'Connected to {server.conn_addr}')

                skip_prompt = True
                while skip_prompt or UI.prompt_follow_up_action() != FollowUpAction.RETURN_HOME:
                    server.notify_client() if not skip_prompt else None
                    skip_prompt = False
                    filepath = UI.get_file()
                    spinner: SpinnerThread = UI.get_spinner('Sending File')
                    server.transfer_file(filepath)
                    UI.stop_spinner(spinner)
                    print("Done")

                server.notify_client(dispose=True)
                server.dispose()
                return

    def init_client(self):
        with Client(self.ip) as client:
            spinner: SpinnerThread = UI.get_spinner("Finding devices")
            hosts = client.scan_network(self.network_ip)
            UI.stop_spinner(spinner)
            if len(hosts) == 0:
                print("No devices found to receive files from")
            server_ip = UI.prompt_hosts(hosts)
            client.connect(server_ip)

            while client.is_connected:
                spinner: SpinnerThread = UI.get_spinner('Receiving File')
                client.receive_file()
                UI.stop_spinner(spinner)
                print('Done')
                spinner: SpinnerThread = UI.get_spinner('Waiting for sender')
                client.listen_server_status()
                UI.stop_spinner(spinner)

            print("Connection closed by sender")


if __name__ == "__main__":
    app = Connect()
    app.start()
