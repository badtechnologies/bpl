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
        self.width = 80
        self.height = 24
        self.term = None

    def write(self, data):
        self.channel.sendall(data.encode())

    def read(self, size=-1):
        return self.channel.recv(size).decode()

    def readline(self, size=65536):
        while b"\n" not in self.buffer:
            data = self.channel.recv(1024)
            if not data: return ""
            self.buffer += data

        line, self.buffer = self.buffer.split(b"\n", 1)
        return line.decode() + "\n"

    def flush(self):
        return  # paramiko handles data flushing

    def close(self):
        self.channel.close()

    def get_size(self):
        return self.width, self.height

    def is_interactive(self):
        return True


class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.user = None
        self.command = None

    def check_channel_exec_request(self, channel, command):
        self.command = command.decode()
        self.event.set()
        return True

    def check_auth_password(self, username, password):
        userman = UserManager()
        self.user = userman.get_user_by_credentials(username, password)

        return paramiko.common.AUTH_SUCCESSFUL if self.user else paramiko.common.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.common.OPEN_SUCCEEDED
        return paramiko.common.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        self.term = term.decode()
        self.width = width
        self.height = height

        return True


class SSHDaemon:
    def __init__(self, console: Session, host_key=paramiko.RSAKey(filename=get_shell_path("cfg", "badbandssh_rsa_key")), port=2200):
        self.host_key = host_key
        self.port = port
        self.console = console

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

        try:
            shell = Shell(Session(SSHTerminal(channel), server.user))
            if server.command:
                shell.run_line(server.command)
            else:
                shell.start()
        except Exception as e:
            self.console.io.println(f"BadBandSSH session error: {e}")

        channel.close()
        transport.close()


def main(session: Session, args: list[str]):
    SSHDaemon(session).start()
