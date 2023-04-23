
import socket
from dnslib.server import BaseResolver
from dnslib import *
import itertools


# Configuration parameters
DNS_PORT = 53
DNS_DOMAIN = 'example.com'
DNS_IPS = ['192.168.1.1', '192.168.1.2']

# DNS resolver class
class MyResolver(BaseResolver):
    def __init__(self, domain, ips):
        self.domain = domain
        self.ips = ips
        self.ip_cycle = itertools.cycle(self.ips)

    def resolve(self, request, handler):
        reply = DNSRecord(request)

        qname = request.q.qname
        if str(qname) == self.domain:
            # Retrieve the next IP from the IP cycle
            ip = next(self.ip_cycle)

            reply.add_answer(*RR.fromZone(f"{self.domain} 60 IN A {ip}"))

        return reply

# DNS server class
class DNSServer:
    def __init__(self, port, resolver):
        self.port = port
        self.resolver = resolver

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', self.port))
        print(f"DNS server listening on port {self.port}")

        while True:
            data, addr = sock.recvfrom(512)
            request = DNSRecord.parse(data)
            reply = self.resolver.resolve(request, addr)

            if reply:
                sock.sendto(reply.pack(), addr)

# Create and start the DNS server
resolver = MyResolver(DNS_DOMAIN, DNS_IPS)
server = DNSServer(DNS_PORT, resolver)
server.start()
