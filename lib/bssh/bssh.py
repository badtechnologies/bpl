import socket
import threading
from threading import Thread

import paramiko
from bdsh import get_shell_path
from bdsh.io import TerminalIO
from bdsh.session import Session
from bdsh.shell import Shell
from bdsh.user import UserManager


class SSHTerminal(TerminalIO):
    def __init__(self, channel: paramiko.Channel):
        self.channel = channel
        self.buffer = b''

    def write(self, data):
        self.channel.sendall(data.encode())

    def read(self, size=-1):
        return self.channel.recv(size).decode()

    def readline(self, size=65536):
        data = b''
        while not data.endswith(b'\n') and len(data) < size:
            data += self.channel.recv(1)
        return data.decode()

    def flush(self):
        return  # paramiko handles data flushing

    def close(self):
        self.channel.close()

    def get_size(self):
        return None

    def is_interactive(self):
        return True


class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.user = None

    def check_auth_password(self, username, password):
        userman = UserManager()
        user = userman.get_user_by_credentials(username, password)

        return paramiko.common.AUTH_SUCCESSFUL if user else paramiko.common.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.common.OPEN_SUCCEEDED
        return paramiko.common.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


class SSHDaemon:
    def __init__(self, host_key=paramiko.RSAKey(filename=get_shell_path("cfg", "badbandssh_rsa_key")), port=2200):
        self.host_key = host_key
        self.port = port

    def start(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", self.port))
        sock.listen(100)

        while True:
            client, addr = sock.accept()
            Thread(target=self.handle, args=(client,)).start()

    def handle(self, client):
        transport = paramiko.Transport(client)
        transport.add_server_key(self.host_key)

        server = SSHServer()
        transport.start_server(server=server)
        channel = transport.accept(30)
        if channel is None: return

        server.event.wait(10)
        if not server.event.is_set(): return

        shell = Shell(Session(SSHTerminal(channel), server.user))
        shell.start()

        channel.close()
        transport.close()


def main(session: Session, args: list[str]):
    SSHDaemon().start()
