# -*- coding: utf-8 -*-
"""
devices.py (c) 2010 by Pascal Schuppli

Setzt auf wxgraph auf und stellt virtuelle Netzwerk-Komponenten zur Verfügung,
welche in einem Graph zu einem simulierten Netzwerk zusammengeschaltet werden
können.
"""

import random

import wxgraph
import wx
import routing
import gui


BROADCASTMAC = "FF:FF:FF:FF:FF:FF"

class NodeModel(object):
    """Eigentlich nur ein Sammelbehälter für diverse Attribute von Knoten"""
    def __init__(self):
        self.onlineState = True

    def setOnlineState(self, state):
        self.onlineState = state

    def getOnlineState(self):
        return self.onlineState


def buildRandomMAC():
    """Erzeugt eine zufällige MAC-Adresse, in der der einfacheren Lesbarkeit halber die 6 Blöcke jeweils aus doppelten Ziffern bestehen"""
    digits = ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99', 'AA', 'BB', 'CC', 'DD', 'EE', 'FF']
    parts = []
    for part in range(6):
        parts.append(random.choice(digits))
    return ":".join(parts)



class EthernetDevice(wxgraph.EdgeConnector):
    """Ein EthernetDevice ist ein EdgeConnector, der einen Endpunkt einer Kante zwischen
       zwei Knoten darstellt. Dies modelliert die realen Gegebenheiten recht gut; Hosts
       und Router können ja ebenfalls über mehrere Netzwerkkarten verfügen."""
    def __init__(self, node, ip=None, subnetmask=None):
        super(EthernetDevice, self).__init__(node)
        self.mac = buildRandomMAC()
        self.ipaddr = ip
        self.subnetmask = subnetmask
        if node:
            node.addDevice(self)
        
    def getOnlineState(self):
        return self.node.model.onlineState

    onlineState = property(getOnlineState, doc='Gibt an, ob dieses Device online ist oder nicht (Status wird von zugehörigem Knoten geholt)')

    def onReceivePacket(self, packet):
        """Handler, der bei Ankunft eines Pakets an diesem Gerät aufgerufen
           wird. Pakete werden per Voreinstellung bei Ankunft an den eigentlichen
           Knoten weitergereicht; dieser kann immer noch feststellen, auf welchem
           EthernetDevice das Paket einging, da das Ziel-Attribut des Pakets ja auf
           das EtherDevice verweist."""

        if self.acceptPacket(packet):
            self.node.onReceivePacket(packet)
            

    def acceptPacket(self, packet):
        """Gibt True zurück, wenn dieses Paket angenommen werden sollte. Gründe
           für die Ablehnung eines Pakets sind, dass das Gerät offline ist oder
           dass die Ziel-MAC-adresse des Pakets nicht der MAC-Adresse des 
           Geräts entspricht. (Es gibt noch keinen promiscious mode)"""
        return self.onlineState and (packet.destmac == BROADCASTMAC or packet.destmac == self.mac)
  

class Switch(wxgraph.GraphNode):
    def __init__(self, x, y):
        super(Switch, self).__init__(x, y, model = NodeModel())
        self.fillcolor = "#ffcc33"
        self.model.mactable = {}

        self.contextmenu = m = wx.Menu()
        self.contextMenuHandler = self.onContextMenu
        
        viewmactable = wx.NewId()
        m.Append(viewmactable, "&Portzuordnung")

        # Binde die beiden Kontextmenüeinträge an Methoden
        self.bindCommand(viewmactable, self.onViewMACTableCommand)

    def onReceivePacket(self, packet):

        # Can't accept packets if we are down
        if not self.model.onlineState:
            return
        
        # Update mac table
        self.model.mactable[packet.sourcemac] = packet.origin
        print "Switch: Lerne Link für mac ", packet.sourcemac
        
        # Broadcaste das Paket, wenn die Ziel-MAC entweder unbekannt oder die Broadcast-
        # Adressse ist. Ansonsten schicke es an das Ziel, das wir in der MAC-Tabelle
        # gespeichert haben
        if packet.destmac == BROADCASTMAC or packet.destmac not in self.model.mactable:
            print "Switch: Broadcaste (", packet.destmac, ")"
            self.broadcastPacket(packet)
        else:
            print "Switch: Ich kenne den Link für mac ", packet.destmac
            clone = packet.cloneContents(self, self.model.mactable[packet.destmac])
            self.parent.addTraveller(clone)

    def broadcastPacket(self, packet):
        for edge in self.edges:
            opposite = edge.oppositeTo(self)
            if opposite != packet.origin:
                clone = packet.cloneContents(self, opposite)
                self.parent.addTraveller(clone)

    def paintNode(self, gc):
        """Erweitert paintNode der Elternklasse dahingehend, dass je nach online-
           Zustand des Knotens entweder grau (offline) oder die vorgesehene Füll-
           farbe (online) zum Färben des Knotens verwendet wird."""
        online = self.model.getOnlineState()
       
        if not online:
            backup = self.fillcolor
            self.fillcolor = "#aaaaaa"

        super(Switch, self).paintNode(gc)

        if not online:
            self.fillcolor = backup

    def onViewMACTableCommand(self, contextitem):
        gui.onViewMACTable(self)

class Router(wxgraph.GraphNode):
    def __init__(self, x, y, devlist):
        super(Router, self).__init__(x, y, model = NodeModel())
        self.fillcolor = "#3333ff"
        # Routen
        self.model.routes = []
        # Konfigurationsdaten der Ethernet-Devices
        self.model.devs = []
        # ARP Queue beinhaltet alle Pakete, die auf ein MAC warten
        self.model.arpqueue = []
        # ARP Cache
        self.model.arpcache = {}

        # Some statistics: Number of packets for this host
        self.model.inboundpackets = 0
        self.model.forwardedpackets = 0
        
        for dev in devlist:
            self.model.devs.append([dev[0], dev[1], dev[2]])
            dev[2].node = self
            self.connectors.append(dev[2])
            # Lokale Netze werden automatisch in Routingtabelle geschrieben
            myip = routing.binaryIP(dev[0])
            mymask = routing.binaryIP(dev[1])
            mynet = myip & mymask
            self.model.routes.append(routing.Route(routing.binaryIP2String(mynet), dev[1], None, 10, len(self.connectors)-1))

        # Kontext-Menü für Hosts
        self.contextmenu = m = wx.Menu()
        self.contextMenuHandler = self.onContextMenu
        m.AppendCheckItem(10001, "Online")
        m.Append(10002, "&ARP-Request senden")
        m.Append(10003, "&IP-Paket senden")
        m.Append(10004, "&Routingtabelle")
        m.Append(10005, "ARP &Cache")
        m.Append(10006, "&Statistik löschen")

        # Binde die beiden Kontextmenüeinträge an Methoden
        self.bindCommand(10001, self.onOnlineStateCommand)
        self.bindCommand(10002, self.onSendPacketCommand)
        self.bindCommand(10003, self.onSendIPPacketCommand)
        self.bindCommand(10004, self.onEditRoutingTableCommand)
        self.bindCommand(10005, self.onViewARPCacheCommand)
        self.bindCommand(10006, self.onClearStatsCommand)

    def addDevice(self,device):
        """Fügt ein EthernetDevice zu diesem Router hinzu."""
        self.model.devs.append([device.ipaddr, device.subnetmask, device])
        self.connectors.append(device)
        # Route für dieses Netz hinzufügen
        myip = routing.binaryIP(device.ipaddr)
        mymask = routing.binaryIP(device.subnetmask)
        mynet = myip & mymask
        self.model.routes.append(routing.Route(routing.binaryIP2String(mynet), device.subnetmask, None, 10, len(self.connectors)-1))



    def paintNode(self, gc):
        """Erweitert paintNode der Elternklasse dahingehend, dass je nach 
           online-Zustand des Knotens entweder grau (offline) oder die 
           vorgesehene Füll-farbe (online) zum Färben des Knotens verwendet 
           wird."""

        online = self.model.getOnlineState()
        
        if not online:
            backup = self.fillcolor
            self.fillcolor = "#aaaaaa"

        super(Router, self).paintNode(gc)

        if (self.model.inboundpackets > 0 or self.model.forwardedpackets > 0 or len(self.model.arpqueue) > 0):
            mx, my = self.position()
            font = gc.CreateFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL), "#555555")
            gc.SetFont(font)
            gc.DrawText("In: " + str(self.model.inboundpackets), mx+self.radius*1.5,my-5)
            text = "Fwd: " + str(self.model.forwardedpackets)
            if len(self.model.arpqueue) > 0:
                text = text + " Q: " + str(len(self.model.arpqueue))
            gc.DrawText(text, mx+self.radius*1.5, my+5)

        if not online:
            self.fillcolor = backup

    def clearPacketStatistics(self):
        self.model.inboundpackets = 0
        self.model.forwardedpackets = 0
       
    def onReceivePacket(self, packet):
        if not self.model.onlineState:
            return

        payload = None

        if isinstance(packet, EthernetFrame):
            payload = packet.payload

        if payload and isinstance(payload, IPPacket):
            print "Router: Eingehendes IP-Paket für", payload.destip, "(TTL", payload.ttl, ")"
            payload.ttl -= 1
            if payload.ttl > 0:
                self.handleIPPacket(payload, packet.dest)
            return
                
        if type(packet) == ARPRequest and self.hasIP(packet.destip):
            dev = self.devForIP(packet.destip)
            self.parent.addTraveller(ARPReply(dev[2], packet.origin, dev[2].mac, packet.sourcemac, dev[0], packet.sourceip))

        if type(packet) == ARPReply:
            self.processARPReply(packet)

    def appendToARPQueue(self, ip, packet):
        self.model.arpqueue.append((ip, packet))

    def processARPReply(self, ethernetFrame):
        """Nimmt ein Mapping IP->MAC in den ARPCache auf und verschickt dann
        diejenigen Pakete in der arpqueue, welche auf diese MAC-Adresse
        gewartet haben."""

        ip = ethernetFrame.sourceip
        srcmac = ethernetFrame.sourcemac
        srcdev = ethernetFrame.origin
        destdev = ethernetFrame.dest

        # ARP Cache erweitern
        self.model.arpcache[ip] = srcmac

        # Pakete, die auf diese MAC gewartet haben, verschicken
        handled = []
        for pair in self.model.arpqueue:
            queryip, packet = pair[0], pair[1]
            if queryip == ip:
                handled.append(pair)
                self.model.forwardedpackets += 1
                self.sendEthernetFrame(destdev, srcdev, srcmac, packet)
                print "Got MAC for my packet to", ip, ":", srcmac
        
        # Verschickte Pakete aus der Queue entfernen
        for pair in handled:
            self.model.arpqueue.remove(pair)

    def handleIPPacket(self, packet, device=None):
        
        if self.hasIP(packet.destip):
            self.handleIncomingPacket(packet)
            return

        if device:
            myip, mymask, dummy = self.configForDev(device)
            if routing.isSameSubnet(myip, packet.destip, mymask):
                print "Router: Ich route keine Pakete innerhalb eines Subnetzes!"
                return
       
        self.forwardPacket(packet)

    def handleIncomingPacket(self, packet):
        """Behandle ein Paket, das für diesen Host bestimmt ist."""
        self.model.inboundpackets += 1
        print "Hurrah, ein (IP)-Paket für mich!"

    def forwardPacket(self, packet):
        """Leite ein Paket, das nicht für uns bestimmt ist, gemäss der Routing-
           tabelle an ein anderes Ziel weiter."""

        candidates = routing.routesTo(self.model.routes, packet.destip)

        if len(candidates) > 0:
            route = candidates[0]

            # Lokales Austragen des Pakets... d.h. wir suchen die MAC der
            # Zieladresse... wenn die Route einen Gateway aufweist, müssen
            # wir stattdessen die MAC-Adresse des Gateways ausfindig machen.
            if route.gw == None:
                ip = packet.destip
            else:
                ip = route.gw
        
            packet.sourceip = self.model.devs[route.link][0]
            self.sendIPPacket(packet, route.link, ip)
            
        else:
            print "Router: Ich habe keine Route zu", packet.destip

    def sendIPPacket(self, packet, devicenr, ip):
        """Verschickt das IP-Paket packet über device an ip. Wenn ip
           nicht im arpcache liegt, wird zuerst ein ARP-Request generiert
           und das Paket in die arpqueue gelegt."""

        device = self.connectors[devicenr]

        if ip in self.model.arpcache:
            self.sendEthernetFrame(device, self.getOppositeTo(device), self.model.arpcache[ip], packet)
            self.model.forwardedpackets += 1
        else:
            self.appendToARPQueue(ip, packet)
            self.parent.addTraveller(ARPRequest(device, self.getOppositeTo(device), device.mac, self.model.devs[devicenr][0], ip)) 
            
    def sendEthernetFrame(self, srcdev, destdev, destmac, payload):
        """Schickt payload von srcdev nach destdev mit Zielmac destmac"""
        frame = EthernetFrame(srcdev, destdev, srcdev.mac, destmac, payload)
        self.parent.addTraveller(frame)
     
    def onRightClick(self, event):
        item = self.contextmenu.FindItemById(10001)
        if item.IsChecked() != self.model.getOnlineState():
            item.Toggle()
        super(Router, self).onRightClick(event)
       
   
    def onOnlineStateCommand(self, contextItem):
        self.model.setOnlineState(contextItem.IsChecked())

    def onClearStatsCommand(self, contextItem):
        self.clearPacketStatistics()
        self.parent.repaint()
        self.parent.Update()

    def onSendPacketCommand(self, contextItem):
        gui.onSendARPRequest(self)

    def onSendIPPacketCommand(self, contextItem):
        gui.onSendIPPacket(self)

    def onEditRoutingTableCommand(self, contextItem):
        gui.onEditRoutingTable(self)

    def onViewARPCacheCommand(self, contextItem):
        gui.onViewARPCache(self)

    def hasIP(self, ip):
        """Sieht nach, ob eines der EthernetDevices des Routers die IP ip hat"""
        if self.devForIP(ip):
            return True
        else:
            return False

    def devForIP(self, ip):
        """Liefert das Tripel (ip, netzmaske, device) für eine IP-Adresse"""
        for triple in self.model.devs:
            if triple[0] == ip:
                return triple
        return None

    def configForDev(self, dev):
        """Liefert das Konfigurationstripel (ip, netzmaske, connector) für
           den Connector dev"""
        for triple in self.model.devs:
            if triple[2] == dev:
                return triple
        return None

    def ipForDev(self, dev):
        """Liefert die IP-Adresse des Devices dev"""
        for triple in self.model.devs:
            if triple[2] == dev:
                return dev[0]
        return None

    def subnetmaskForDev(self, dev):
        """Liefert die Subnetzmaske des Devices dev"""
        for triple in self.model.devs:
            if triple[2] == dev:
                return dev[1]
        return None


class Host(Router):
    """Ein Host unterscheidet sich von einem Router eigentlich nur dadurch,
       dass wir davon ausgehen, dass er nur in einem Netz steht bzw. nur
       eine Netzwerkkarte hat."""
    def __init__(self, x, y, ip, subnetmask):
        super(Host, self).__init__(x, y, [(ip, subnetmask, EthernetDevice(None))])
        self.fillcolor = "green"
       
       
class EthernetFrame(wxgraph.EdgeTraveller):
    "Ein Ethernet-Frame."""
    def __init__(self, n1, n2, sourcemac, destmac, payload):
        super(EthernetFrame, self).__init__((n1, n2), name = destmac, color = "#aaaa22", onArrival = n2.onReceivePacket)
        self.sourcemac = sourcemac
        self.destmac = destmac
        self.payload = payload

    def cloneContents(self, origin, dest):
        return EthernetFrame(origin, dest, self.sourcemac, self.destmac, self.payload)
        
class IPPacket(object):
    """Ein IP-Paket."""
    def __init__(self, sourceip, destip, payload):
        self.sourceip = sourceip
        self.destip = destip
        self.ttl = 15
        self.payload = payload

class ARPRequest(wxgraph.EdgeTraveller):
    """Ein ARP-Request ist ein Ethernet-Frame, der an die Broadcast-MAC 
       verschickt wird, um eine IP-Adresse im lokalen Netz ausfindig zu 
       machen."""
    def __init__(self, n1, n2, sourcemac, sourceip, destip):
        super(ARPRequest, self).__init__((n1, n2), name = "wer hat " + destip + "?", color = "#22aa22", onArrival = n2.onReceivePacket)
        self.sourcemac = sourcemac
        self.destmac = BROADCASTMAC
        self.sourceip = sourceip
        self.destip = destip
    def cloneContents(self, origin, dest):
        return ARPRequest(origin, dest, self.sourcemac, self.sourceip, self.destip)

class ARPReply(wxgraph.EdgeTraveller):
    """Ein ARP-Reply ist die Antwort auf einen ARP-Request und wird von dem-
       jenigen Gerät verschickt, das die im ARP-Request gesuchte IP-Adresse
       hält."""
    def __init__(self, n1, n2, sourcemac, destmac, sourceip, destip):
        super(ARPReply, self).__init__((n1, n2), name = sourceip + " ist bei " + sourcemac, color = "#22aa22", onArrival = n2.onReceivePacket)
        self.sourcemac = sourcemac
        self.destmac = destmac                                        
        self.sourceip = sourceip
        self.destip = destip
    def cloneContents(self, origin, dest):
        return ARPReply(origin, dest, self.sourcemac, self.destmac, self.sourceip, self.destip)
       
        



   
