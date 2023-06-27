import re

from src import colors

def shady_os_api_calls(filename, os_type='all'):
    # Windows API calls
    shady_win_calls = ['accept','AddCredentials','bind','CertDeleteCertificateFromStore',
    'CheckRemoteDebuggerPresent','CloseHandle','closesocket','connect','ConnectNamedPipe',
    'CopyFile','CreateFile','CreateProcess','CreateToolhelp32Snapshot','CreateFileMapping',
    'CreateRemoteThread','CreateDirectory','CreateService','CreateThread','CryptEncrypt',
    'DeleteFile','DeviceIoControl','DisconnectNamedPipe','DNSQuery','EnumProcesses',
    'ExitProcess','ExitThread','FindWindow','FindResource','FindFirstFile','FindNextFile',
    'FltRegisterFilter','FtpGetFile','FtpOpenFile','GetCommandLine','GetComputerName',
    'GetCurrentProcess','GetThreadContext','GetDriveType','GetFileSize','GetFileAttributes',
    'GetHostByAddr','GetHostByName','GetHostName','GetModuleHandle','GetModuleFileName',
    'GetProcAddress','GetStartupInfo','GetSystemDirectory','GetTempFileName','GetTempPath',
    'GetTickCount','GetUpdateRect','GetUpdateRgn','GetUserNameA','GetUrlCacheEntryInfo',
    'GetVersionEx','GetWindowsDirectory','GetWindowThreadProcessId','HttpSendRequest',
    'HttpQueryInfo','IcmpSendEcho','IsBadReadPtr','IsBadWritePtr','IsDebuggerPresent',
    'InternetCloseHandle','InternetConnect','InternetCrackUrl','InternetQueryDataAvailable',
    'InternetGetConnectedState','InternetOpen','InternetQueryDataAvailable','InternetQueryOption',
    'InternetReadFile','InternetWriteFile','LdrLoadDll','LoadLibrary','LoadLibraryA','LockResource',
    'listen','MapViewOfFile','OutputDebugString','OpenFileMapping','OpenProcess','Process32First',
    'Process32Next','recv','ReadFile','RegCloseKey','RegCreateKey','RegDeleteKey','RegDeleteValue',
    'RegEnumKey','RegOpenKey','ReadProcessMemory','send','sendto','SetFilePointer','SetKeyboardState',
    'SetWindowsHook','ShellExecute','Sleep','socket','StartService','TerminateProcess','UnhandledExceptionFilter',
    'URLDownload','VirtualAlloc','VirtualFree','VirtualProtect','VirtualAllocEx','WinExec','WriteProcessMemory',
    'WriteFile','WSASend','WSASocket','WSAStartup','ZwQueryInformation'
    ]

    # Linux System calls
    shady_linux_calls = [
        'fork',           # Create a child process
        'vfork',          # Create a child process and block parent
        'clone',          # Create a child process
        'execve',         # Execute program
        'ptrace',         # Process trace
        'kill',           # Send signal to a process
        'tkill',          # Send signal to a thread
        'exit',           # Terminate the calling process
        'exit_group',     # Terminate all threads in the calling process
        'getuid',         # Get user identity
        'geteuid',        # Get effective user identity
        'getgid',         # Get group identity
        'getegid',        # Get effective group identity
        'reboot',         # Reboot or enable/disable Ctrl-Alt-Del
        'unshare',        # Disassociate parts of the process execution context
        'chroot',         # Change root directory
        'pivot_root',     # Change the root filesystem
        'mount',          # Mount filesystem
        'umount2',        # Unmount filesystem
        'swapon',         # Start/stop swapping to file/device
        'swapoff',        # Start/stop swapping to file/device
        'setns',          # Reassociate thread with a namespace
        'futex',          # Fast user-space locking
        'mmap',           # Map or unmap files or devices into memory
        'munmap',         # Map or unmap files or devices into memory
        'mprotect',       # Set protection on a region of memory
        'mknod',          # Create a special or ordinary file
        'chdir',          # Change working directory
        'fchdir',         # Change working directory
        'open',           # Open and possibly create a file
        'close',          # Close a file descriptor
        'creat',          # Create a new file or rewrite an existing one
        'link',           # Make a new name for a file
        'unlink',         # Delete a name and possibly the file it refers to
        'symlink',        # Make a new name for a file
        'chmod',          # Change permissions of a file
        'chown',          # Change ownership of a file
        'lchown',         # Change ownership of a file
        'fchown',         # Change ownership of a file
        'pipe',           # Create pipe
        'dup',            # Duplicate a file descriptor
        'dup2',           # Duplicate a file descriptor
        'dup3',           # Duplicate a file descriptor
        'sendfile',       # Transfer data between file descriptors
        'splice',         # Splice data to/from a pipe
        'vmsplice',       # Splice user pages into a pipe
        'socket',         # Create a socket
        'bind',           # Bind a name to a socket
        'connect',        # Initiate a connection on a socket
        'listen',         # Listen for connections on a socket
        'accept',         # Accept a connection on a socket
        'getsockname',    # Get socket name
        'getpeername',    # Get name of connected peer
        'socketpair',     # Create a pair of connected sockets
        'send',           # Send a message on a socket
        'sendto',         # Send a message on a socket
        'recv',           # Receive a message from a socket
        'recvfrom',       # Receive a message from a socket
        'shutdown',       # Shut down part of a full-duplex connection
        'setsockopt',     # Set options on sockets
        'getsockopt',     # Get options on sockets
        'sendmsg',        # Send a message on a socket
        'recvmsg',        # Receive a message from a socket
        'readahead',      # Preload file pages into page cache
        'fadvise64',      # Predeclare an access pattern for file data
        'flock',          # Apply or remove an advisory lock on an open file
        'fsync',          # Sync file to disk
        'fdatasync',      # Sync file data, not metadata, to disk
        'truncate',       # Truncate or extend a file to a specified length
        'ftruncate',      # Truncate or extend a file to a specified length
        'getdents',       # Get directory entries
        'getcwd',         # Get current working directory
        'chown',          # Change ownership
        'chdir',          # Change directory
        'fchdir',         # Change directory
        'rename',         # Change the name or location of a file
        'mkdir',          # Create a directory
        'rmdir',          # Remove a directory
        'creat',          # Create a file
        'link',           # Create a file hard link
        'unlink',         # Delete a name and the file it refers to
        'symlink',        # Create a symbolic link
        'readlink',       # Read the target of a symbolic link
        'chmod',          # Change permissions of a file
        'fchmod',         # Change permissions of a file
        'chown',          # Change ownership of a file
        'fchown',         # Change ownership of a file
        'lchown',         # Change ownership of a file
        'umask',          # Set file mode creation mask
        'getrlimit',      # Get resource limit
        'getrusage',      # Get resource usage
        'sysinfo',        # Return system information
        'times',          # Get process times
        'ptrace',         # Process trace
        'getuid',         # Get user identity
        'syslog',         # Read and/or clear kernel message ring buffer; set console_loglevel
        'getgid',         # Get group identity
        'setuid',         # Set user identity
        'setgid',         # Set group identity
        'geteuid',        # Get effective user identity
        'getegid',        # Get effective group identity
        'setpgid',        # Set process group
        'getppid',        # Get parent process ID
        'getpgrp',        # Get process group
        'setsid',         # Create session and set process group
        'setreuid',       # Set real and/or effective user ID
        'setregid',       # Set real and/or effective group ID
        'getgroups',      # Get supplementary group IDs
        'setgroups',      # Set supplementary group IDs
    ]
    
    shady_calls = shady_win_calls + shady_linux_calls
    
    api_calls = []

    with open(filename) as f:
        file_content = f.read().lower()

        for shady_call in shady_calls:
            # Check for the pattern of a function call (e.g., 'func(', 'func (', 'func\n(')
            if re.search(r'\b{}\s*\('.format(shady_call.lower()), file_content):
                api_calls.append(shady_call)

    if api_calls:
        for call in api_calls:
            print(colors.BRed + "Suspicious API was found: {}\n".format(call) + colors.RESET)
    else:
        print(colors.BGreen + "\nNo suspicious API call was found.\n" + colors.RESET)