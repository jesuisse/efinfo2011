
class Route(object):
    def __init__(self, destination, netmask, gateway, metric, link):
        self.dest = destination
        self.netmask = netmask
        self.gw = gateway
        self.metric = metric
        self.link = link

    def __str__(self):
        if self.gw == None:
            gw = "*"
        else:
            gw = self.gw
        return self.dest.ljust(20) + self.netmask.ljust(20) + gw.ljust(20) +  str(self.metric).rjust(4)        

    def __repr__(self):
        return "<Route " + self.dest + " " + self.netmask + " at " + hex(id(self)) +">"

def binaryIP(string):
    """Konvertiert eine textliche Darstellung einer IP-Adresse wie z.B.
       192.0.32.10 in die binäre Darstellung als int-Wert."""

    parts = string.split(".")
    if len(parts) != 4:
        raise ValueError("Ungültiges Format (erwartet: xxx.xxx.xxx.xxx)")

    ip = 0
    n = 0
    for part in parts:
        try:
            n = int(part)
        except ValueError:
            raise ValueError("Ungültiges Format des Adressteils '" + part + "'") 

        if n < 0 or n > 255:
            raise ValueError("Wertebereich muss 0-255 sein")
        
        ip = (ip << 8) + n

    return ip

def binaryIP2String(binip):
    parts = []
    for x in range(4):
        parts.append(str(binip & 255))
        binip = binip >> 8;
    parts.reverse()
    return '.'.join(parts)

def isValidIP(string):
    try:
        val = binaryIP(string)
        return True
    except ValueError:
        return False

def isSameSubnet(ip1, ip2, subnetmask):
    binip1 = binaryIP(ip1)
    binip2 = binaryIP(ip2)
    mask = binaryIP(subnetmask)

    return (binip1 & mask) == (binip2 & mask)
   


def printRoute(route):
    print route        

def printRoutes(routes):
    print "Ziel".ljust(19), "Maske".ljust(19), "Gateway".ljust(16), " Metrik"
    for route in routes:
        printRoute(route)

def pardown(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0

def routeSortingComparator(a, b):
    """Sortiert zwei Routen a und b priorisiert nach Netzmaske, Ziel und
       Metrik, so dass die konkreteste und beste Route am Anfang steht."""
    return pardown((binaryIP(b.netmask) - binaryIP(a.netmask))) \
           or pardown((binaryIP(a.dest) - binaryIP(b.dest))) \
           or (a.metric - b.metric)

def sortRoutes(table):
    """Sortiert sämtliche Routen in table (in place!); je spezifischer 
       eine Route ist, desto weiter oben landet sie. Die Sortierung erfolgt
       deshalb priorisiert nach Netzmaske, Ziel und Metrik."""
    table.sort(cmp = routeSortingComparator)
     
def addRoute(table, route):

    table.append(route)

    sortRoutes(table)


def routesTo(routes, ip):
    """Findet Routen für Packete mit Zieladresse ip, beste Route zuerst."""

    bip = binaryIP(ip)

    candidates = []

    for route in routes:
        net = binaryIP(route.dest)
        mask = binaryIP(route.netmask)

        if bip & mask == net:
            candidates.append(route)
            
    return candidates


def init(routes):
    addRoute(routes, Route("192.168.1.0", "255.255.255.0", "192.168.1.1", 100, None))
    addRoute(routes, Route("192.168.0.0", "255.255.0.0", "192.168.2.1", 1, None))
    addRoute(routes, Route("192.168.2.0", "255.255.255.0", "192.168.0.1", 75, None))
    addRoute(routes, Route("192.168.1.0", "255.255.255.0", "192.168.1.1", 50, None))
    addRoute(routes, Route("0.0.0.0", "0.0.0.0", "192.168.0.1", 1, None))

routes=[]
init(routes)

    
