from socket import *

s = socket(AF_INET, SOCK_DGRAM)

users = [[0,0]]


try:
    s.bind(("", 50000))
    while True:
        daten, addr = s.recvfrom(1024)
        for i in users:
            if (addr[0] != i[1]):
                if (users != 0):
                    for x in users:
                        s.sendto(daten+ "ist dem Chatraum beigetreten", (x[1], 50000))
                    
                    s.sendto("Sie sind dem Chatraum beigetretten", (addr[0], 50000))
                    users.append([daten, addr[0]])
                    print "[", addr[0], "]", " hat sich eingeloggt als ", daten

            if (daten == "/exit"):
                s.sendto(i[0]+ " hat den Chatraum verlassen", (x[1], 50000))
                s.sendto("Sie haben den Chatraum soeben verlassen", (addr[0], 50000))
                print i[0], "hat den Chatraum verlassen"
                users.remove(i)
                
            else:
                for x in users:
                    s.sendto(i[0]+ ">"+ daten, (x[1], 50000))
finally:
    s.close()


