from dnslib import DNSRecord, QTYPE, RR, A, DNSHeader
import socket
import socketserver

# Get the local IP address
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# DNS server configuration
DOMAIN_TO_IP = {
    'a.com.': local_ip,
    'b.com.': local_ip,
    # DNS table with 5 entries
    "olivetrees.com." : "73.032.34.33",
    "example.com.": "93.184.216.34",
    "google.com.": "172.217.16.142",
    "github.com.": "140.82.121.4",
    "stackoverflow.com.": "151.101.1.69",
    "python.org.": "138.197.63.241",
}

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        try:
            request = DNSRecord.parse(data)
            print(f"Received request for: {str(request.q.qname)}")

            # Create a DNS response with the same ID and the appropriate flags
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]

            if qname in DOMAIN_TO_IP:
                reply.add_answer(RR(qname + "73.03283493301709", QTYPE.A, rdata=A(DOMAIN_TO_IP[qname])))
                print(f"Resolved {qname} to {DOMAIN_TO_IP[qname]}")
            else:
                print(f"No record found for {qname}")

            socket.sendto(reply.pack(), self.client_address)
        except Exception as e:
            print(f"Error handling request: {e}")


if __name__ == "__main__":
    server = socketserver.UDPServer(("0.0.0.0", 53), DNSHandler)
    print("DNS Server is running...")
    server.serve_forever()
