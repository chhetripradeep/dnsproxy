import logging
import socket

from .proxy import UDPProxy

logger = logging.getLogger(__name__)


class UDP(object):
    """
    UDP server implementation.

    Listens on UDP endpoint and forwards clients to proxy.
    """

    def __init__(self, hostname='127.0.0.1', port=53, destination='1.1.1.1:853'):
        self.hostname = hostname
        self.port = port
        self.destination = destination

    def handle(self, client):
        proc = UDPProxy(client, self.destination)
        proc.daemon = True
        proc.start()
        logger.debug('Started process %r to handle connection' % (proc))

    def run(self):
        try:
            logger.info('Starting udp server on port %d' % self.port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.hostname, self.port))
            while True:
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.handle(client)
        except Exception as e:
            logger.exception('Exception while running the server %r' % e)
        finally:
            logger.info('Closing server socket')
            self.socket.close()