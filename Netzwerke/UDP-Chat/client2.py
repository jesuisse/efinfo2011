from socket import *
s = socket(AF_INET, SOCK_DGRAM)

ip = raw_input("IP-Adresse:")
nachricht = raw_input("Nachricht: ")


s.sendto(nachricht, (ip, 50000))

antwort, addr = s.recvfrom(1024)

print "[", addr[0], "]", antwort

s.close()

