import netsim.gui
app = netsim.gui.wxinit()

from netsim.netsetup import *

switch1 = makeSwitch()

host1 = makeHost("192.168.1.10", "255.255.255.0")
host2 = makeHost("192.168.1.11", "255.255.255.0")
host3 = makeHost("192.168.1.15", "255.255.255.0")
host4 = makeHost("192.168.1.16", "255.255.255.0")
host5 = makeHost("192.168.1.17", "255.255.255.0")

for host in host1, host2, host3, host4, host5:
    connect(host, switch1)

nodes = [host1, host2, host3, host4, host5,
         switch1]

positions = [(30,50), (160, 90), (20, 280), (560, 20), (450, 360),
             (250, 180)]

setPositions(nodes, positions)

"""
Kommentare entfernen, um beim Start automatisch Pakete zu generieren
packets = [
    ARPRequest(nodes[8], nodes[7], nodes[8].mac, "192.168.2.2", "192.168.2.1"), 
    ARPRequest(nodes[0], nodes[3], nodes[8].mac, "192.168.1.2", "192.168.1.1") ]
"""

packets = []
frame = None

# Mit Knoten und Paketen initialisieren und Netzwerksimulation starten
if __name__ == '__main__':
    netsim.gui.init(nodes, packets, application = app)




        
