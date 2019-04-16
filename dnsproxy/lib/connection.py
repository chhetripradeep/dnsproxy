import logging

logger = logging.getLogger(__name__)


class Connection(object):
    """TCP server/client connection abstraction."""

    def __init__(self, type):
        self.buffer = b''
        self.closed = False
        self.type = type        # server or client

    def send(self, data):
        return self.conn.send(data)

    def recv(self, bytes=8192):
        try:
            data = self.conn.recv(bytes)
            if len(data) == 0:
                logger.debug('Received 0 bytes from %s' % self.type)
                return None
            logger.debug('Received %d bytes from %s' % (len(data), self.type))
            return data
        except Exception as e:
            logger.exception(
                'Exception while receiving from connection %s %r with reason %r' % (self.type, self.conn, e))
            return None

    def close(self):
        self.conn.close()
        self.closed = True

    def buffer_size(self):
        return len(self.buffer)

    def has_buffer(self):
        return self.buffer_size() > 0

    def queue(self, data):
        self.buffer += data

    def flush(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
        logger.debug('Flushed %d bytes to %s' % (sent, self.type))