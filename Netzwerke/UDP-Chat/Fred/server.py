from socket import *
import time
import datetime
import re

def logoffChat(ip):
    """logs off user by ip """
    pass
    
def getNickByIP(ip):
    """gets nickname by ip"""
    pass
    
def serverBroadcast(message):
    """sends message to everyone by server with message"""
    
    
def sendMessage(message)
    """sends message to everyone by user (with an array, message[0] is time, 1 ip and 2 text)"""
    # TODO: checks whether ip already there & more escapes
    pass

def isEscapeCharacter(message):
    escape = re.match(r'/exit', message[2])
    if escape:
        return True
    
    else: 
        return False


s = socket(AF_INET, SOCK_DGRAM)

try:
    s.bind(("", 50000))
    while True:
        daten, addr = s.recvfrom(1024)
        message = [int(time.time()), addr[0], daten ]
        
        if isEscapeCharacter(message):
            logoffChat(message[1])
            serverBroadcast(getNickbyIP(message[1]), "hat den Chat verlassen.")
        
        sendMessage(message)
finally:
    s.close()


