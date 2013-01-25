
from netsim.devices import Host, Switch, Router, EthernetDevice
from wxgraph import addEdge
import netsim.gui

app = netsim.gui.wxinit()

def linkHostTo(host, node):
    addEdge(host.getConnector(0), node)


nodes = [ Host(30,50, "192.168.1.10", "255.255.255.0"),
          Host(160, 90, "192.168.1.11", "255.255.255.0"),
          Host(20, 280, "192.168.1.15", "255.255.255.0"),
          Switch(100,180),
          Router(400, 200, [("192.168.2.1", "255.255.255.248", EthernetDevice(None)), ("10.1.0.2", "255.255.0.0", EthernetDevice(None)), ("10.1.4.2", "255.255.255.0", EthernetDevice(None))]),
          Router(390, 320, [("10.1.0.1", "255.255.0.0", EthernetDevice(None)), ("10.2.0.1", "255.255.0.0", EthernetDevice(None)), ("10.3.0.1", "255.255.255.252", EthernetDevice(None))]),
          Router(250, 350, [("192.168.1.1", "255.255.255.0", EthernetDevice(None)), ("10.2.0.2", "255.255.0.0", EthernetDevice(None))]),
          Switch(520, 120),
          Host(560, 20, "192.168.2.2", "255.255.255.248"),
          Host(650, 160, "192.168.2.3", "255.255.255.248"),
          Router(550,320, [("10.1.4.1", "255.255.255.0", EthernetDevice(None)), ("10.3.0.2", "255.255.255.252", EthernetDevice(None))]), 
          Router(500,500, [("10.3.0.1", "255.255.255.0", EthernetDevice(None))]), 
          ]


linkHostTo(nodes[0], nodes[3])
linkHostTo(nodes[1], nodes[3])
linkHostTo(nodes[2], nodes[3])
addEdge(nodes[3], nodes[6].getConnector(0))
addEdge(nodes[4].getConnector(1), nodes[5].getConnector(0))
addEdge(nodes[5].getConnector(1), nodes[6].getConnector(1))
addEdge(nodes[4].getConnector(0), nodes[7])
linkHostTo(nodes[8], nodes[7])
linkHostTo(nodes[9], nodes[7])
addEdge(nodes[4].getConnector(2), nodes[10].getConnector(0))
addEdge(nodes[5].getConnector(2), nodes[10].getConnector(1))

#addEdge(nodes[4].getConnector(0), nodes[10])
#addEdge(nodes[5], nodes[11])
#addEdge(nodes[6], nodes[11])
#addEdge(nodes[10], nodes[11])

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




        
