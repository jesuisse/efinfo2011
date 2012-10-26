from socket import *

s = socket(AF_INET, SOCK_DGRAM)

ip = raw_input("IP-Adresse des Servers")
nick = raw_input("Nick: ")

s.sendto(nick, (ip, 50000))
s.close()

s = socket(AF_INET, SOCK_DGRAM)

try:
    s.bind(("", 50001))
    while True:
        daten, addr = s.recvfrom(1024)
        print "[", addr[0], "]", daten
finally:
    s.close()
    
