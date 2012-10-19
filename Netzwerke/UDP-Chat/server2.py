from socket import *

print "Hallo! Hier ist dein freundlicher Echo-Server!"
print "Warte auf Verbindungen..."

s = socket(AF_INET, SOCK_DGRAM)

try:
    s.bind(("", 50000))
    while True:
        daten, addr = s.recvfrom(1024)
        print "[", addr[0], "]", daten
        s.sendto("Hi, ich bins, dein Echo: " + daten, addr)
finally:
    s.close()
    
