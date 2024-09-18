import netifaces as ni

def get_ip():
    
    try:
        ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    except KeyError:
        ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
    except:
        ip = '127.0.0.1' # fallback

    return ip
