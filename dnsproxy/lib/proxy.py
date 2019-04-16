import logging
import multiprocessing

from .server import Server

logger = logging.getLogger(__name__)


class TCPProxy(multiprocessing.Process):
    """
    TCP Proxy Implementation.

    Accepts TCP connections and forwards it to destination.
    """

    def __init__(self, client, destination):
        super(TCPProxy, self).__init__()

        self.client = client
        self.destination = destination

    def forward(self):
        destination = self.destination.split(':')
        host = destination[0]
        port = int(destination[1])

        self.server = Server(host, port)

        try:
            logger.debug('Connecting to upstream server %s:%s' % (host, port))
            self.server.connect()
        except Exception as e:
            logger.exception('Exception while connection with reason %r' % e)

        try:
            logger.debug('Sending data to upstream server %s:%s' % (host, port))
            self.server.send(self.mesg)
        except Exception as e:
            logger.exception('Exception while sending data with reason %r' % e)

        try:
            logger.debug('Receiving data from upstream server %s:%s' % (host, port))
            self.response = self.server.recv()
            logger.debug('Received msg: %r' % self.response)
        except Exception as e:
            logger.exception('Exception while receiving data with reason %r' % e)

        try:
            logger.debug('Sending back the response to connection %r at address %r' % (self.client.conn, self.client.addr))
            self.client.send(self.response)
        except Exception as e:
            logger.exception('Exception while sending back data with reason %r' % e)

    def process(self):
        try:
            self.mesg = self.client.recv()
            logger.debug('Received msg: %r' % self.mesg)
        except Exception as e:
            logger.exception('Exception while processing data for connection %r with reason %r' % (self.client.conn, e))

        self.forward()

    def run(self):
        logger.debug('Proxying connection %r at address %r' % (self.client.conn, self.client.addr))
        try:
            self.process()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.exception('Exception while handling connection %r with reason %r' % (self.client.conn, e))
        finally:
            self.client.conn.close()
            logger.debug('Closing proxy for connection %r at address %r' % (self.client.conn, self.client.addr))


class UDPProxy(multiprocessing.Process):
    """
    UDP Proxy Implementation.

    Accepts UDP connections and forwards it to destination.
    """

    def __init__(self, client, destination):
        super(UDPProxy, self).__init__()

        self.client = client
        self.destination = destination

    def forward(self):
        destination = self.destination.split(':')
        host = destination[0]
        port = int(destination[1])

        self.server = Server(host, port)

        try:
            logger.debug('Connecting to upstream server %s:%s' % (host, port))
            self.server.connect()
        except Exception as e:
            logger.exception('Exception while connection with reason %r' % e)

        try:
            logger.debug('Sending data to upstream server %s:%s' % (host, port))
            self.server.send(self.mesg)
        except Exception as e:
            logger.exception('Exception while sending data with reason %r' % e)

        try:
            logger.debug('Receiving data from upstream server %s:%s' % (host, port))
            self.response = self.server.recv()
            logger.debug('Received msg: %r' % self.response)
        except Exception as e:
            logger.exception('Exception while receiving data with reason %r' % e)

        try:
            logger.debug('Sending back the response to connection at address %r' % (self.client.addr))
            self.client.send(self.response)
        except Exception as e:
            logger.exception('Exception while sending back data with reason %r' % e)

    def process(self):
        try:
            self.mesg = self.client.recv()
            logger.debug('Received msg: %r' % self.mesg)
        except Exception as e:
            logger.exception('Exception while processing data for connection with reason %r' % (e))

        self.forward()

    def run(self):
        logger.debug('Proxying connection at address %r' % (self.client.addr))
        try:
            self.process()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.exception('Exception while handling connection with reason %r' % (e))
        finally:
            self.client.close()
            logger.debug('Closing proxy for connection at address %r' % (self.client.addr))