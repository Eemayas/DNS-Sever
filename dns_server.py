import dnslib
import dns.zone
import dns.resolver
import dns.rcode
import dns.rdatatype
import socketserver

# Define the domain name and zone file path
DOMAIN = 'google.com.'
ZONE_FILE = './zone.txt'

# Load the zone data from the zone file
zone = dns.zone.from_file(ZONE_FILE, DOMAIN)

# Define the DNS request handler class
class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive the DNS request data
        data = self.request[0]
        # Extract the client IP address and port number
        client_ip = self.client_address[0]
        client_port = self.client_address[1]
        # Parse the DNS request data into a DNS message object
        request = dnslib.DNSRecord.parse(data)
        # Get the requested domain name
        domain = str(request.q.qname)
        # Check if the domain name is in the zone
        if domain in zone:
            # Create a DNS response message object
            response = dnslib.DNSRecord()
            response.add_question(request.q)
            # Add the resource records for the requested domain name
            for name, ttl, rdata in zone[domain].rdatasets:
                rr = dnslib.RR.fromZone(f"{name} {ttl} {rdata}")
                response.add_answer(rr)
            # Send the DNS response to the client
            self.socket.sendto(response.pack(), (client_ip, client_port))
        else:
            # If the domain name is not in the zone, query the recursive resolver
            resolver = dns.resolver.Resolver()
            response = None
            try:
                response = resolver.query(domain, rdtype=request.q.qtype)
            except dns.resolver.NXDOMAIN:
                # If the domain name does not exist, return a DNS "NXDOMAIN" error
                response = dnslib.DNSRecord()
                response.header.rcode = dns.rcode.NXDOMAIN
                response.add_question(request.q)
            except Exception:
                pass
            if response is not None:
                # Create a DNS response message object based on the response from the recursive resolver
                response = dnslib.DNSRecord.parse(response.to_wire())
                # Send the DNS response to the client
                self.socket.sendto(response.pack(), (client_ip, client_port))

# Define the DNS server class
class DNSServer(socketserver.UDPServer):
    allow_reuse_address = True

# Start the DNS server
if __name__ == '__main__':
    server = DNSServer(('0.0.0.0', 53), DNSHandler)
    server.serve_forever()
