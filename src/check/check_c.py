import re
from src import colors

def check_c(filename):
    with open(filename, 'r') as f:
        buf = f.read()
        regex = re.findall('ctypes', buf)
        print(regex)
        if regex!=[]:
            print(colors.BRed + "Ctypes found. Suspicious import." + colors.RESET)
        else:
            print(colors.BGreen + "Ctypes wasn't found." + colors.RESET)

