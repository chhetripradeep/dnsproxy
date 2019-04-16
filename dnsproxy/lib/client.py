from .connection import Connection


class Client(Connection):
    """Accepts DNS request from client connection."""

    def __init__(self, conn, addr):
        super(Client, self).__init__(b'client')
        self.conn = conn
        self.addr = addr