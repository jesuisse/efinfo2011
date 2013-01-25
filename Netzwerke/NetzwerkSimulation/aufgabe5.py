import netsim.gui
app = netsim.gui.wxinit()

from netsim.netsetup import *

switch1 = makeSwitch()

host1 = makeHost("192.168.1.11", "255.255.255.0")
host2 = makeHost("192.168.1.12", "255.255.255.0")
host3 = makeHost("192.168.1.13", "255.255.255.0")

router1 = makeRouter()
router1_dev1 = EthernetDevice(router1, "192.168.1.1", "255.255.255.0")
router1_dev2 = EthernetDevice(router1, "10.1.0.2", "255.255.0.0")

switch2 = makeSwitch()

host4 = makeHost("192.168.2.2", "255.255.255.248")
host5 = makeHost("192.168.2.3", "255.255.255.248")

router2 = makeRouter()
router2_dev1 = EthernetDevice(router2, "192.168.2.1", "255.255.255.248")
router2_dev2 = EthernetDevice(router2, "10.2.0.2", "255.255.0.0")

router3 = makeRouter()
router3_dev1 = EthernetDevice(router3, "10.1.0.1", "255.255.0.0")
router3_dev2 = EthernetDevice(router3, "10.2.0.1", "255.255.0.0")

# Ersten Switch anschliessen
for host in host1, host2, host3:
    connect(host, switch1)
connect(router1_dev1, switch1)

# Zweiten Switch anschliessen
for host in host4, host5:
    connect(host, switch2)
connect(router2_dev1, switch2)

# Router miteinander verbinden
connect(router1_dev2, router3_dev1)
connect(router2_dev2, router3_dev2)

nodes = [host1, host2, host3, host4, host5, 
         switch1, switch2,
         router1, router2, router3]

positions = [(30,50), (160, 90), (20, 280), (560, 20), (650, 160),
             (100, 180), (520, 120),
             (250, 350), (400, 200), (390, 320)]

setPositions(nodes, positions)

packets = [
    netsim.gui.generateARPRequest(host1, "192.168.1.12")
]


# Zeile entfernen, um mit Standard-Paketversand zu beginnen
packets = []

frame = None

# Mit Knoten und Paketen initialisieren und Netzwerksimulation starten
if __name__ == '__main__':
    netsim.gui.init(nodes, packets, application = app)




        
