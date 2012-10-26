# -*- coding: utf-8 -*-
from socket import *

# Hier speichern wir die Liste der Clients
clientList = [ ]

def makeClient(ip, name):
    """Erzeugt einen Eintrag für die Client-Liste aus IP-Adresse
       und dem Nickname des Clients""" 
    return [ip, name]

def getIP(client):
    """Liefert aus einem einzelnen Eintrag der Client-Liste die IP-
       Adresse."""
    return client[0]

def getNick(client):
    """Liefert aus einem einzelnen Eintrag der Client-Liste den
       Nickname"""
    return client[1]

def findClientByIP(ip):
    """Findet in der Client-Liste den Eintrag mit der IP-Adresse ip
       und liefert ihn zurück (oder None, wenn kein solcher Eintrag
       existiert)"""
    global clientList
    for client in clientList:
        if getIP(client) == ip:
            return client
    return None

def removeClient(ip):
    """Entfernt den Eintrag mit der IP-Adresse ip aus der Client-
       Liste"""
    global clientList
    for client in clientList:
        if getIP(client) == ip:
            clientList.remove(client)
            return

def sendToClients(sock, message):
    """Sendet eine Nachricht (message) an sämtliche verbundenen 
       Clients unter Verwendung des sockets sock"""
    global clientList
    for client in clientList:
        s.sendto(message, (getIP(client), 50001))
    print "Sent to everyone:", message

    
s = socket(AF_INET, SOCK_DGRAM)

name = raw_input("Name des Servers:")

try:
    s.bind(("", 50000))
    while True:
	# Daten und Quelle von Socket lesen
        daten, addr = s.recvfrom(1024)
	# Versuchen, aufgrund der Quelle den Client zu identifizieren
        client = findClientByIP(addr[0])            
        if client == None:
	    # IP des Senders der Daten noch nicht bekannt, also neuen
            # Client-Eintrag erzeugen und alle informieren
            clientList.append(makeClient(addr[0], daten))
            sendToClients(s, "Neu Online: " + daten)
        elif daten == "/exit":
	    # Nachricht ist exit-Kommando, also Client entfernen und
            # alle informieren
            removeClient(addr[0])
            sendToClients(s, getNick(client) + " ist jetzt offline.")
        else:
	    # Normale Nachricht eines bereits bekannten clients, allen
            # Clients weiterleiten
            sendToClients(s, getNick(client) + ": " + daten)
finally:
    s.close()
    
