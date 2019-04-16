import socket
import ssl

from .connection import Connection


class Server(Connection):
    """Establishes connection to upstream DNS server."""

    def __init__(self, host, port):
        super(Server, self).__init__(b'server')
        self.addr = (host, int(port))

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = ssl.wrap_socket(self.sock)
        self.conn.connect((self.addr[0], self.addr[1]))