from scapy.all import *
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def dns_query(domain, server_ip):
    try:
        dns_req = IP(dst='127.0.0.1', src="127.0.0.1")/UDP(dport=53, sport=3001)/DNS(rd=1, qd=DNSQR(qname=domain))
        answer = sr1(dns_req, verbose=0, timeout=2)
        if answer and answer.haslayer(DNS):
            if answer[DNS].ancount > 0:
                return answer[DNS].an.rdata
            else:
                return "No answer section in the response"
        elif answer:
            return f"Received non-DNS response: {answer.summary()}"
        else:
            return "No response received"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    server_ip = get_local_ip()
    print(f"Using DNS server IP: {server_ip}")

    domains = ["example.com", "google.com", "github.com", "stackoverflow.com", "python.org", "nonexistent.com", "olivetrees.com"]

    for domain in domains:
        result = dns_query(domain, server_ip)
        print(f"{domain}: {result}")
