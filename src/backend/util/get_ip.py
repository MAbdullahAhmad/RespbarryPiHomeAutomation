import socket
import netifaces as ni
from scapy.all import ARP, Ether, srp

# Function to get the current IP address of the device
def get_ip():
    try:
        ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    except ValueError:
        try:
            ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
        except:
            ip = '127.0.0.1'  # fallback
    return ip

# Function to scan the network and return active IPs
def get_active_ips(network_range):
    arp_request = ARP(pdst=network_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    active_ips = []
    for sent, received in answered_list:
        active_ips.append(received.psrc)
    
    return active_ips

# Function to check if a specific port is open
def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Set a timeout of 1 second
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

# Main function to discover IPs with ports 8000 and 3000 open
def discover_pis_with_open_ports():
    current_ip = get_ip()
    
    # Replace the last part of the IP address with 0/24 for scanning the subnet
    network_base = '.'.join(current_ip.split('.')[:-1]) + '.0/24'

    active_ips = get_active_ips(network_base)
    pis_with_ports = []

    for ip in active_ips:
        if is_port_open(ip, 8000) and is_port_open(ip, 3000):
            pis_with_ports.append(ip)
    
    return pis_with_ports

if __name__ == "__main__":
    discovered_ips = discover_pis_with_open_ports()
    
    if discovered_ips:
        print("Found devices with ports 8000 and 3000 open:")
        for ip in discovered_ips:
            print(ip)
    else:
        print("No devices found with both ports 8000 and 3000 open.")
