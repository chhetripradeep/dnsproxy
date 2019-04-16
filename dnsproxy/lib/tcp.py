import logging
import socket

from .client import Client
from .proxy import TCPProxy

logger = logging.getLogger(__name__)


class TCP(object):
    """
    TCP server implementation.

    Listens on TCP endpoint and forwards clients to proxy.
    """

    def __init__(self, hostname='127.0.0.1', port=53, destination='1.1.1.1:853', backlog=100):
        self.hostname = hostname
        self.port = port
        self.destination = destination
        self.backlog = backlog

    def handle(self, client):
        proc = TCPProxy(client, self.destination)
        proc.daemon = True
        proc.start()
        logger.debug('Started process %r to handle connection %r' % (proc, client.conn))

    def run(self):
        try:
            logger.info('Starting tcp server on port %d' % self.port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.hostname, self.port))
            self.socket.listen(self.backlog)
            while True:
                conn, addr = self.socket.accept()
                logger.debug('Accepted connection %r at address %r' % (conn, addr))
                client = Client(conn, addr)
                self.handle(client)
        except Exception as e:
            logger.exception('Exception while running the server %r' % e)
        finally:
            logger.info('Closing server socket')
            self.socket.close()