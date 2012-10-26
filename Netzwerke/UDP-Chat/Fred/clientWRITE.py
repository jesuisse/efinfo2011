from socket import *

s = socket(AF_INET, SOCK_DGRAM)

ip = raw_input("IP-Adresse des Servers:")
print "Bitte beachte, dass zuerst clientREAD mit dem Server verbunden werden muss"
print "Viel Spass beim Chatten"
nachricht = raw_input("Nachricht: ")

while True
	nachricht = raw_input("--> ")
	s.sendto(nachricht, (ip, 50000))

s.close()

