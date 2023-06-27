import re
import socket
from base64 import urlsafe_b64encode
from virustotal_python import Virustotal
from src import colors

API_KEY = "1c62432c1e1aef05078aba9db67036682fd79d6790c3794cdbb63cdb0c4480b2"

def is_website(site):
    """Check if site is reachable."""
    try:
        # Strip off the protocol
        site = re.sub(r'^https?://', '', site)

        host = socket.gethostbyname(site)
        socket.create_connection((host, 80), 2)
        return True
    except:
        return False

def extract_urls(filename):
    """Extract URLs from a given file."""
    with open(filename) as f:
        content = f.read()

    url_pattern = re.compile(r'(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))?')
    urls = url_pattern.findall(content)
    return [url for url in urls if is_website(url)]


def url_reputation(filename):
    """Check the reputation of URLs using VirusTotal API."""
    urls = extract_urls(filename)
    vtotal = Virustotal(API_KEY=API_KEY)

    for url in urls:
        url_id = urlsafe_b64encode(url.encode()).decode().strip("=")
        report = vtotal.request(f"urls/{url_id}")
        
        # Any negative reputation score indicates a potentially malicious URL
        if report.data['attributes']['reputation'] < 0:
            print(colors.BRed + "{} may be malicious (reputation score: {})".format(url, report.data['attributes']['reputation']) + colors.RESET)

        # A URL is malicious if it is detected by more than half of the antivirus engines
        total_engines = len(report.data['attributes']['last_analysis_stats'])
        malicious_detections = report.data['attributes']['last_analysis_stats']['malicious']

        if malicious_detections > total_engines / 2:
            print(colors.BRed + "{} is detected as malicious by {} out of {} antivirus engines".format(url, malicious_detections, total_engines) + colors.RESET)
    
    print(colors.BPurple + "URL reputation check complete." + colors.RESET)




