#!/usr/bin/env python

import argparse
import logging

from .lib import tcp
from .lib import udp
from multiprocessing import Process

logger = logging.getLogger(__name__)


def get_ip_port(socket):
    """Takes in a socket and returns ip address and port"""

    try:
        socket = socket.split(':')
        host = socket[0]
        port = int(socket[1])
        return host, port
    except Exception as e:
        logger.exception('Exception while parsing input with reason %r' % e)
        return None


def tcp_listener(host, port, dest):
    try:
        tcp_proxy = tcp.TCP(host, port, dest)
        tcp_proxy.run()
    except KeyboardInterrupt:
        pass


def udp_listener(host, port, dest):
    try:
        udp_proxy = udp.UDP(host, port, dest)
        udp_proxy.run()
    except KeyboardInterrupt:
        pass


def main():
    """Entry-point of the DNS to DNS-over-TLS Proxy"""

    parser = argparse.ArgumentParser(
        description='DNS to DNS-over-TLS Proxy'
    )

    parser.add_argument('--bind-addr', dest='bindaddr', default='localhost:53', help='default: localhost:53')
    parser.add_argument('--dns-addr', dest='dnsaddr', default='1.1.1.1:853', help='default: 1.1.1.1:853')
    parser.add_argument('--log-level', default='INFO', help='DEBUG, INFO, WARNING, ERROR, CRITICAL')

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level),
                        format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')

    bindhost, bindport = get_ip_port(args.bindaddr)

    processes = []
    listeners = [tcp_listener, udp_listener]

    try:
        for listener in listeners:
            process = Process(target=listener, args=(bindhost, bindport, args.dnsaddr))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()