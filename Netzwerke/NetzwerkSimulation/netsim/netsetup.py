from netsim.devices import Host, Router, Switch, EthernetDevice
from wxgraph import addEdge

def connect(node1, node2):
    if isinstance(node1, Host):
        node1 = node1.getConnector(0)
    if isinstance(node2, Host):
        node2 = node2.getConnector(0)
    addEdge(node1, node2)
    
def setPositions(nodes, positions):
    for node, pos in zip(nodes, positions):
        node.setPosition(pos[0], pos[1])
                        
def makeHost(ip, subnet, pos = None):
    if pos:
        return Host(pos[0], pos[1], ip, subnet)
    else:
        return Host(0,0,ip, subnet)

def makeRouter(devices = [], pos = None):
    if pos:
        return Router(pos[0], pos[1], devices)
    else:
        return Router(0,0, devices)

def makeSwitch(pos = None):
    if pos:
        return Switch(pos[0], pos[1])
    else:
        return Switch(0,0)
