import re

from src import colors

def find_antidebug_functions(file, functions):
    response = list()
    for line in file:
        for func in functions:
            if re.search(r'\b' + func + r'\b', line, re.I):  # case-insensitive search
                response.append(func)
    return response

def antidebug(filename):
    anti_debug_functions = ['CheckRemoteDebuggerPresent', 'FindWindow',
                           'GetWindowThreadProcessId', 'IsDebuggerPresent',
                           'OutputDebugString', 'Process32First', 'Process32Next',
                           'TerminateProcess', 'UnhandledExceptionFilter',
                           'ZwQueryInformation','NtQueryInformationProcess',
                           'NtSetInformationThread']

    try:
        with open(filename, 'r') as f:
            suspicious_functions = find_antidebug_functions(f, anti_debug_functions)
    except FileNotFoundError:
        print('File not found: {}'.format(filename))
        return

    if suspicious_functions:
        for func in suspicious_functions:
            print(colors.BRed + "Suspicious anti-debug function was found: {}\n".format(func) + colors.RESET)
    else:
        print(colors.BGreen + "\nNo suspicious anti-debug function was found.\n" + colors.RESET)
