import dns.resolver
import dns.update

# Define the DNS server's IP address and port
server_ip = '192.168.0.1'
server_port = 53

# Create a resolver object and specify the server details
resolver = dns.resolver.Resolver()
resolver.nameservers = [server_ip]
resolver.port = server_port

# Define the DNS record to be added
new_record = dns.rdataset.from_text('example.com.', 300, 'IN', 'A', '192.168.0.2')

# Create an update object and add the new record to it
update_obj = dns.update.Update('example.com.')
update_obj.add(new_record)

# Perform the DNS update using the update() method of the resolver object
response = resolver.update(update_obj)

# Check the status of the update operation
if response.rcode() != dns.rcode.NOERROR:
    print('Error:', dns.rcode.to_text(response.rcode()))
else:
    print('DNS record added successfully.')
