import socket

def check_internet_connection():
    try:
        host = socket.gethostbyname("www.gooogle.com")
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False