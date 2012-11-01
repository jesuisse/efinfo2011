import netsim.gui
app = netsim.gui.wxinit()

from netsim.netsetup import *

switch1 = makeSwitch()

host1 = makeHost("192.168.1.10", "255.255.255.0")
host2 = makeHost("192.168.1.11", "255.255.255.0")
host3 = makeHost("192.168.1.15", "255.255.255.0")
host4 = makeHost("192.168.1.16", "255.255.255.0")
host5 = makeHost("192.168.1.17", "255.255.255.0")

switch2 = makeSwitch()
host6 = makeHost("192.168.1.20", "255.255.255.0")
host7 = makeHost("192.168.1.21", "255.255.255.0")
host8 = makeHost("192.168.1.22", "255.255.255.0")
host9 = makeHost("192.168.1.23", "255.255.255.0")

for host in host1, host2, host3, host4, host5:
    connect(host, switch1)

for host in host6, host7, host8, host9:
    connect(host, switch2)

connect(switch1, switch2)

nodes = [host1, host2, host3, host4, host5,
         host6, host7, host8, host9,
         switch1, switch2]

positions = [(30,50), (160, 90), (20, 280), (260, 20), (250, 360),
             (400, 320), (370, 500), (570, 480), (590, 260),
             (250, 180), (550, 340)]

setPositions(nodes, positions)

packets = [
    netsim.gui.generateARPRequest(host9, "192.168.1.11")
]

#packets = []
frame = None

# Mit Knoten und Paketen initialisieren und Netzwerksimulation starten
if __name__ == '__main__':
    netsim.gui.init(nodes, packets, application = app)




        
