import re, requests
from src import colors

VIRUSTOTAL_API_KEY = "1c62432c1e1aef05078aba9db67036682fd79d6790c3794cdbb63cdb0c4480b2"

def check_ip_reputation(filename):
    # Define the regex pattern for IP addresses
    pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

    # Initialize the list object
    ip_list = []

    # Open and read the file line by line
    with open(filename, "r") as f:
        for line in f:
            # Extract the IP addresses
            results = pattern.findall(line)
            if results:
                ip_list.extend(results)

    # Check each IP address against the VirusTotal API
    for ip in ip_list:
        try:
            response = requests.get(
                f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
                headers={"x-apikey": VIRUSTOTAL_API_KEY},
            )
            response.raise_for_status()
            data = response.json()["data"]
            score = data["attributes"]["reputation"]
            if score < -5:
                print(colors.BRed + f"{ip} is a malicious IP." + colors.RESET)
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 401:
                print("Error: Invalid API key.")
            else:
                print(f"Error: {error}")
        except Exception as error:
            print(f"Error: {error}")

    print(colors.BPurple + "IP reputation check complete." + colors.RESET)
