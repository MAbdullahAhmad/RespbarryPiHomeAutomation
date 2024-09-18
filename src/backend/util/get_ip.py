import netifaces as ni

def get_ip():
    try:
        ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    except KeyError:
        ip = 'No IP found'
    return ip

print(f"IP Address: {get_ip()}")
