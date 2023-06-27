import argparse, os, sys

from src import colors
from src.check import ipreputation, calls, entropy, antidebug, urls, antivm, emails, file, dynamic
from src.check_updates import check_internet_connection

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Security Vulnerabilities Finder with Static Analysis")
    parser.add_argument("filename", help="/path/to/file")


    args = parser.parse_args()
    

    print(colors.BPurple + """
███████╗██╗   ██╗███████╗███████╗ █████╗  Security
██╔════╝██║   ██║██╔════╝██╔════╝██╔══██╗ Vulnerabilities
███████╗██║   ██║█████╗  ███████╗███████║ Finder with
╚════██║╚██╗ ██╔╝██╔══╝  ╚════██║██╔══██║ Static
███████║ ╚████╔╝ ██║     ███████║██║  ██║ Analysis
╚══════╝  ╚═══╝  ╚═╝     ╚══════╝╚═╝  ╚═╝
                                         """
+ colors.RESET)

internet_connection = check_internet_connection.check_internet_connection()

if (not internet_connection):
    print(colors.BRed + "There is no Internet connection.\nTerminating." + colors.RESET)
    sys.exit()


# Make the location of SVFSA the working directory
py_file_location = os.path.dirname(__file__)
args.filename = os.path.realpath(args.filename)
if py_file_location:
    os.chdir(py_file_location)

# IP checks
# ipreputation.check_ip_reputation(args.filename)

# URL/domain checks
urls.url_reputation(args.filename)

# Virustotal DB scan
# file.file_upload(args.filename)

# Shady Windows API calls
# calls.shady_os_api_calls(args.filename)

# Entropy for obfuscation (of sections)
# entropy.entropy(args.filename)

# Anti-debug Techniques
# antidebug.antidebug(args.filename)

# Anti-virtualization techniques
# antivm.antivm(args.filename)


### Dynamic Analysis
# dest = 'dynamicvm:password@192.168.16.129:/home/dynamicvm/DynAnal'
# ssh_dest = 'dynamicvm:password@192.168.16.129'
# file_dest = '/home/dynamicvm/DynAnal/dynamic.py'
# dynamic.dynamic_anal(args.filename, file_dest, dest, ssh_dest)
