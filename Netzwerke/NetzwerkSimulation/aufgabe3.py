import netsim.gui
app = netsim.gui.wxinit()

from netsim.netsetup import *

switch1 = makeSwitch()

host1 = makeHost("192.168.1.11", "255.255.255.0")
host2 = makeHost("192.168.1.12", "255.255.255.0")
host3 = makeHost("192.168.1.13", "255.255.255.0")
host4 = makeHost("192.168.1.14", "255.255.255.0")
host5 = makeHost("192.168.1.15", "255.255.255.0")

switch2 = makeSwitch()
host6 = makeHost("192.168.1.21", "255.255.255.0")
host7 = makeHost("192.168.1.22", "255.255.255.0")
host8 = makeHost("192.168.1.23", "255.255.255.0")
host9 = makeHost("192.168.1.24", "255.255.255.0")

switch3 = makeSwitch()
host10 = makeHost("192.168.1.31", "255.255.255.0")
host11 = makeHost("192.168.1.32", "255.255.255.0")
host12 = makeHost("192.168.1.33", "255.255.255.0")
host13 = makeHost("192.168.1.34", "255.255.255.0")

for host in host1, host2, host3, host4, host5:
    connect(host, switch1)

for host in host6, host7, host8, host9:
    connect(host, switch2)

for host in host10, host11, host12, host13:
    connect(host, switch3)

connect(switch1, switch2)
connect(switch1, switch3)
connect(switch2, switch3)

nodes = [host1, host2, host3, host4, host5,
         host6, host7, host8, host9,
         host10, host11, host12, host13,
         switch1, switch2, switch3]

positions = [(30,50), (160, 90), (20, 280), (260, 20), (250, 360),
             (400, 320), (370, 500), (570, 480), (590, 260),
             (450, 80), (590, 140), (630, 200), (580, 40), 
             (250, 180), (550, 340), (530, 180)]

setPositions(nodes, positions)


packets = [
    netsim.gui.generateARPRequest(host1, "192.168.1.21"),
    netsim.gui.generateARPRequest(host7, "192.168.1.11"),
    netsim.gui.generateARPRequest(host12, "192.168.1.34") ]

# Folgende Zeile entfernen, um Standard-Simulation laufen zu lassen
packets = []

frame = None

# Mit Knoten und Paketen initialisieren und Netzwerksimulation starten
if __name__ == '__main__':
    netsim.gui.init(nodes, packets, application = app)




        
