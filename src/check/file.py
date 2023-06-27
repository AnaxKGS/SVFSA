import time
import requests
import urllib.parse

from src import colors

headers = {
    "accept": "application/json",
    "x-apikey": "1c62432c1e1aef05078aba9db67036682fd79d6790c3794cdbb63cdb0c4480b2"
}


def upload_file(filename):
    url = "https://www.virustotal.com/api/v3/files"
    with open(filename, "rb") as f:
        files = {"file": (filename, f, "text/x-python")}
        response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    return response.json()["data"]["id"]

def get_analysis(analysis_id):
    analysis_url = "https://www.virustotal.com/api/v3/analyses/" + analysis_id
    while True:
        response = requests.get(analysis_url, headers=headers)
        response.raise_for_status()
        analysis = response.json()
        if analysis["data"]["attributes"]["status"] == "completed":
            return analysis
        time.sleep(10)  # Wait for a while before next check

def file_upload(filename):
    try:
        analysis_id = upload_file(filename)
        analysis = get_analysis(analysis_id)
        malicious = analysis["data"]["attributes"]["stats"]["malicious"]
        undetected = analysis["data"]["attributes"]["stats"]["undetected"]

        if malicious == 0:
            print(colors.BGreen + "No record of the file was found in databases with known malware.\n" + colors.RESET)
        else:
            print(colors.BRed + "The file was found in {} databases with known malware.\n".format(malicious) + colors.RESET)
        print(colors.BPurple + "Number of databases where the file was undetected: {}\n".format(undetected) + colors.RESET)
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")