from scapy.all import *
import socket
import time
import random


def dns_query(domain, server_ip, source_port):
    try:
        dns_req = IP(dst='127.0.0.1', src="127.0.0.1")/UDP(dport=53533, sport=source_port)/DNS(rd=1, qd=DNSQR(qname=domain))
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

def start_dns_clients():
    server_ip = '127.0.0.1'
    #print(f"Using DNS server IP: {server_ip}")

    domains = ["example.com", "google.com", "github.com", "stackoverflow.com", "python.org", "nonexistent.com", "olivetrees.com"]
    for i in range(10):
        try:
            source_port = random.randint(20000, 30000)
            for domain in domains:
                result = dns_query(domain, server_ip, source_port)
                #print(f"{domain}: {result}")
        except:
            continue # do nothing
        time.sleep(15)

if __name__ == "__main__":
    start_dns_clients()
