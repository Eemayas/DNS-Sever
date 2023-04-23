
import dns.resolver

# Configuration parameters
DNS_DOMAIN = 'geeksforgeeks.org'
DNS_SERVER_IP = '192.168.1.1'

# Send a DNS query to the server
resolver = dns.resolver.Resolver()
resolver.nameservers = [DNS_SERVER_IP]
response = resolver.resolve(DNS_DOMAIN)

# Print the response
for rdata in response:
    print(rdata)

