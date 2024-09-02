from scapy.all import *
import socket

# DNS table with 5 entries
dns_table = {
    b"example.com.": "93.184.216.34",
    b"google.com.": "172.217.16.142",
    b"github.com.": "140.82.121.4",
    b"stackoverflow.com.": "151.101.1.69",
    b"python.org.": "138.197.63.241"
}

def dns_responder(data, addr):
    addr = '127.0.0.1'
    # Convert the received data into a DNS packet using Scapy
    pkt = IP(data)
    print(pkt)

    if (DNS in pkt and pkt[DNS].opcode == 0 and pkt[DNS].ancount == 0):
        print(f"Received query for: {pkt[DNS].qd.qname.decode()}")
        if pkt[DNS].qd.qname in dns_table:
            ip = dns_table[pkt[DNS].qd.qname]
            resp = IP(dst=pkt[IP].src, src=pkt[IP].dst)/\
                   UDP(dport=pkt[UDP].sport, sport=53)/\
                   DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd,
                       an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=10, rdata=ip))

            # Send the response back to the client
            sniff_socket.sendto(bytes(resp), addr)
            print(f"Responded to query for {pkt[DNS].qd.qname.decode()} with {ip}")
        else:
            print(f"No record found for {pkt[DNS].qd.qname.decode()}")
    else:
        print("Unknown error")

if __name__ == "__main__":
    print("Starting DNS server...")
    try:
        # Bind to all interfaces on UDP port 53
        sniff_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sniff_socket.bind(('127.0.0.1', 53))

        while True:
            # Receive data from the socket
            data = sniff_socket.recvfrom(1024)
            # Pass the data and address to the DNS responder function
            print(data)
            dns_responder(data, '127.0.0.1')
    except PermissionError:
        print("Error: You need root privileges to bind to port 53.")
        print("Please run the script with sudo.")
    except Exception as e:
        print(f"An error occurred: {e}")

        print(data)
    except PermissionError:
        print("Error: You need root privileges to run this server.")
        print("Please run the script with sudo.")
    except Exception as e:
        print(f"An error occurred: {e}")
