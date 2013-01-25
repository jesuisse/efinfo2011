import netsim.gui
app = netsim.gui.wxinit()

from netsim.netsetup import *

switch1 = makeSwitch()

host1 = makeHost("192.168.1.11", "255.255.255.0")
host2 = makeHost("192.168.1.12", "255.255.255.0")
host3 = makeHost("192.168.1.13", "255.255.255.0")
host4 = makeHost("192.168.1.14", "255.255.255.0")
host5 = makeHost("192.168.1.15", "255.255.255.0")

router1 = makeRouter()
router1_dev1 = EthernetDevice(router1, "192.168.1.1", "255.255.255.0")
router1_dev2 = EthernetDevice(router1, "192.168.2.1", "255.255.255.248")

switch2 = makeSwitch()

host6 = makeHost("192.168.2.2", "255.255.255.248")
host7 = makeHost("192.168.2.3", "255.255.255.248")
host8 = makeHost("192.168.2.4", "255.255.255.248")

for host in host1, host2, host3, host4, host5:
    connect(host, switch1)
connect(router1_dev1, switch1)

for host in host6, host7, host8:
    connect(host, switch2)
connect(router1_dev2, switch2)

nodes = [host1, host2, host3, host4, host5,
         host6, host7, host8,
         switch1, switch2,
         router1]

positions = [(30,50), (160, 90), (30, 280), (70, 10), (170, 260),
             (560, 20), (650, 160), (470, 90),
             (100, 180), (520, 120),
             (370, 300)]

setPositions(nodes, positions)

packets = []
frame = None

# Mit Knoten und Paketen initialisieren und Netzwerksimulation starten
if __name__ == '__main__':
    netsim.gui.init(nodes, packets, application = app)




        
