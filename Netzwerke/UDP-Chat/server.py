from socket import *

s = socket(AF_INET, SOCK_DGRAM)

try:
    s.bind(("", 50000))
    while True:
        daten, addr = s.recvfrom(1024)
        print "[", addr[0], "]", daten
finally:
    s.close()
    
