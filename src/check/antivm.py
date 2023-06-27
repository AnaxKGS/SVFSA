import re
import os
from src import colors


vm_signatures = {
    "Red Pill":"\x0f\x01\x0d\x00\x00\x00\x00\xc3",
    "VirtualPc trick":"\x0f\x3f\x07\x0b",
    "VMware trick":"VMXh",
    "VMCheck.dll":"\x45\xC7\x00\x01",
    "VMCheck.dll for VirtualPC":"\x0f\x3f\x07\x0b\xc7\x45\xfc\xff\xff\xff\xff",
    "Xen":"XenVMM",
    "Bochs & QEmu CPUID Trick":"\x44\x4d\x41\x63",
    "Torpig VMM Trick": "\xE8\xED\xFF\xFF\xFF\x25\x00\x00\x00\xFF\x33\xC9\x3D\x00\x00\x00\x80\x0F\x95\xC1\x8B\xC1\xC3",
    "Torpig (UPX) VMM Trick": "\x51\x51\x0F\x01\x27\x00\xC1\xFB\xB5\xD5\x35\x02\xE2\xC3\xD1\x66\x25\x32\xBD\x83\x7F\xB7\x4E\x3D\x06\x80\x0F\x95\xC1\x8B\xC1\xC3"
}

vm_strings  = {
    "Virtual Box":"VBox",
    "VMware":"WMvare"
}


def antivm(filename):
    tricks_found = list()

    if not os.path.isfile(filename):
        print(colors.BRed + f"File {filename} does not exist!" + colors.RESET)
        return
    
    try:
        with open(filename, 'r') as f:
            buffer = f.read()
    except Exception as e:
        print(colors.BRed + f"Error reading file: {e}" + colors.RESET)
        return
        
        
    for check in vm_strings:
        match = re.findall(vm_strings[check], buffer, re.IGNORECASE | re.MULTILINE)
        if match:
            tricks_found.append(check)
        
    for signature in vm_signatures:
        if buffer.find(vm_signatures[signature][::-1]) > -1:
            tricks_found.append(signature)
        
    if tricks_found:  
        print(colors.BRed + "Found the following Anti-virtualization tricks:\n" + colors.RESET)
        print(colors.BRed + '\n'.join(tricks_found) + colors.RESET) 
    else:
        print(colors.BGreen + "No Anti-virtualization tricks found!" + colors.RESET)
        