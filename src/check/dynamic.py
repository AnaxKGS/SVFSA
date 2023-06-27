import paramiko
import os
import subprocess

import os
import subprocess

def send_file_to_vm(file, dest):
    # Path to WinSCP.com
    winscp_path = r'C:\"Program Files (x86)\WinSCP\WinSCP.com"'
    print(f'{winscp_path} /command "put {file} {dest}" "exit"')
    result = os.system(f'{winscp_path} /command "open {dest}" "put {file}" "exit"')
    if result == 0:
        print("File sent successfully.")
    else:
        print("Failed to send file.")

def run_file_on_vm(file_dest, ssh_dest):
    # Path to PuTTY's plink
    plink_path = r'C:\"Program Files\PuTTY\plink.exe"'
    result = os.system(f'{plink_path} {ssh_dest} python3 {file_dest}')
    if result == 0:
        print("File ran successfully.")
    else:
        print("Failed to run file.")

def capture_ips(ssh_dest):
    plink_path = r'C:\"Program Files\PuTTY\plink.exe"'
    command = [plink_path, ssh_dest, "tcpdump", "-i", "any", "-n"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    for row in iter(process.stdout.readline, b''):
        line = row.decode('utf-8')  # convert byte to string
        ip_addresses = parse_ip_addresses(line)
        print(f'IP Addresses: {ip_addresses}')

def parse_ip_addresses(line):
    split_line = line.split()
    if 'IP' in split_line:
        index = split_line.index('IP')
        src_dest = split_line[index + 1]
        ip_src, ip_dest = src_dest.split('>')
        ip_src = ip_src.split('.')[0:4]
        ip_dest = ip_dest.split('.')[0:4]
        return ip_src, ip_dest
    return None, None

def dynamic_anal(file, file_dest, dest, ssh_dest):
    send_file_to_vm(file, dest)
    run_file_on_vm(file_dest, ssh_dest)
    capture_ips(ssh_dest)