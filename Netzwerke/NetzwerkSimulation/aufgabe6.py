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
router2_dev2 = EthernetDevice(router2, "10.2.0.2", "255.255.255.0")
router2_dev3 = EthernetDevice(router2, "10.2.1.1", "255.255.255.248")

router3 = makeRouter()
router3_dev1 = EthernetDevice(router3, "10.1.0.1", "255.255.255.0")
router3_dev2 = EthernetDevice(router3, "10.2.0.1", "255.255.255.0")

switch3 = makeSwitch()

host6 = makeHost("10.2.1.18", "255.255.255.248")
host7 = makeHost("10.2.1.19", "255.255.255.248")
host8 = makeHost("10.2.1.20", "255.255.255.248")

switch4 = makeSwitch()
host9 = makeHost("10.2.1.34", "255.255.255.248")
host10 = makeHost("10.2.1.35", "255.255.255.248")


router4 = makeRouter()
router4_dev1 = EthernetDevice(router4, "10.2.1.2", "255.255.255.248")
router4_dev2 = EthernetDevice(router4, "10.2.1.17", "255.255.255.248")
router4_dev3 = EthernetDevice(router4, "10.2.1.33", "255.255.255.248")

# Ersten Switch anschliessen
for host in host1, host2, host3, router1_dev1:
    connect(host, switch1)

# Zweiten Switch anschliessen
for host in host4, host5, router2_dev1:
    connect(host, switch2)

# Dritten Switch anschliessen
for host in host6, host7, host8, router4_dev2:
    connect(host, switch3)

# Vierten Switch anschliessen
for host in host9, host10, router4_dev3:
    connect(host, switch4)

# Router miteinander verbinden
connect(router1_dev2, router3_dev1)
connect(router2_dev2, router3_dev2)

connect(router2_dev3, router4_dev1)

nodes = [host1, host2, host3,
         host4, host5,
         host6, host7, host8,
         host9, host10, 
         switch1, switch2, switch3, switch4,
         router1, router2, router3, router4]

positions = [(30,50), (160, 90), (20, 280),
             (560, 20), (650, 160),
             (680, 250), (690, 350), (610, 390),
             (550, 550), (640, 490),
             (100, 180), (520, 120), (600, 310), (590, 500),
             (250, 350), (400, 200), (390, 320), (520, 300)]

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




        
