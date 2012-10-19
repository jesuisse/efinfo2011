from socket import *
s = socket(AF_INET, SOCK_DGRAM)

ip = raw_input("IP-Adresse:")
nachricht = raw_input("Nachricht: ")

s.sendto(nachricht, (ip, 50000))
s.close()

