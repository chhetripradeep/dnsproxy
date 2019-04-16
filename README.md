## DNSProxy

DNS to DNS-over-TLS Proxy (developed with Python 2.7)

### Setup

- Install this python module

```
$ python setup.py install
```

- You can start the server by running

```
$ sudo dnsproxy
```

By default, this proxy server listens on localhost:53 and forwards all the requests to 1.1.1.1:853

### Options

```
$ dnsproxy --help
usage: dnsproxy [-h] [--bind-addr BINDADDR] [--dns-addr DNSADDR]
                [--log-level LOG_LEVEL]

DNS to DNS-over-TLS Proxy

optional arguments:
  -h, --help            show this help message and exit
  --bind-addr BINDADDR  default: localhost:53
  --dns-addr DNSADDR    default: 1.1.1.1:853
  --log-level LOG_LEVEL
                        DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Testing

- First start the server

```
$ sudo dnsproxy --log-level DEBUG
2019-02-03 17:47:06,123 - INFO - pid:29752 - Starting server on port 53
```

- Send a DNS request over TCP using dig utility

```
$ dig @127.0.0.1 google.com +tcp
; <<>> DiG 9.10.6 <<>> @127.0.0.1 google.com +tcp
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32729
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1452
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 (".........................................................................................................................................................................................................................................................................................................................................................................................................................")
;; QUESTION SECTION:
;google.com.			IN	A

;; ANSWER SECTION:
google.com.		204	IN	A	172.217.27.206

;; Query time: 113 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Sun Feb 03 17:47:07 IST 2019
;; MSG SIZE  rcvd: 468
```