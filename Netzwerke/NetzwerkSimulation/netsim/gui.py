# -*- coding: utf-8 -*-
"""
   gui.py (c) Copyright 2010 by Pascal Schuppli

   Enthält GUI-Klassen wie z.B. den Routingtabellen-Dialog.
"""

import thread
import wxgraph
import wx
import wx.grid as gridlib
import wx.lib.mixins.listctrl as listmix

import devices
import routing

def addOKCancel(parent):
    btnsizer = wx.StdDialogButtonSizer()
    ok = wx.Button(parent, wx.ID_OK)
    ok.SetDefault()
    cancel = wx.Button(parent, wx.ID_CANCEL)
    btnsizer.AddButton(ok)
    btnsizer.AddButton(cancel)
    btnsizer.Realize()

    border = wx.BoxSizer(wx.VERTICAL)
    border.Add(btnsizer, 1, wx.EXPAND | wx.ALL, 10)

    return (border, ok, cancel)
    

class RoutingTableDialog(wx.Dialog):
    """Dialogbox, die die Routing-Tabeller eines Router-Knotens in einem editierbaren Grid darstellt. (Rechtsklick auf Zeilenlabels, um eine Route zu löschen)"""
    def __init__(self, parent, node):        
        wx.Dialog.__init__(self, parent, -1, "Routingtabelle", size=(500,250))

        self.node = node
        ndevices = len(node.connectors)

        self.grid = RoutingTableGrid(self, ndevices, node.model.routes)

        border, ok, cancel = addOKCancel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.grid, 0, wx.EXPAND)
        box.Add(border, 0, wx.EXPAND)

        self.SetSizer(box)
        box.Fit(self)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnOK, ok)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel)

    def OnOK(self, event):
        self.node.model.routes = self.grid.exportRoutes()
        event.Skip()
    
    def OnCancel(self, event):
        event.Skip()


class RoutingDataTable(gridlib.PyGridTableBase):
    def __init__(self, ndevices):
        gridlib.PyGridTableBase.__init__(self)
        self.dataTypes = [ gridlib.GRID_VALUE_STRING,
                           gridlib.GRID_VALUE_STRING,
                           gridlib.GRID_VALUE_STRING,
                           gridlib.GRID_VALUE_NUMBER + ':1,10',
                           gridlib.GRID_VALUE_NUMBER + ':1,' + str(ndevices), ]

        self.colLabels = ('Netzwerk', 'Netzmaske', 'Gateway', 'Metrik', 'Gerät')

        self.data = []

        for y in range(10):
            self.data.append(self._makeEmptyRow())

    def _makeEmptyRow(self):
        return self.GetNumberCols() * ['']
                
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return 5

    def IsEmptyCell(self, row, col):
        return self.data[row][col] == ''
        
    def GetValue(self, row, col):
        return self.data[row][col]
        
    def SetValue(self, row, col, value):
        self.data[row][col] = value

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    def DeleteRows(self, pos, num):
        del self.data[pos:pos+num]
        self.data.append(self._makeEmptyRow())
        return True


class RoutingTableGrid(gridlib.Grid):
    """Der Grid für unsere Routingtabelle. Stellt neben einem Standard-Grid
       ein angepasstes Modell (RoutingDataTable) sowie Import- und Export-
       Funktionen für Routingtabellen zur Verfügung."""

    def __init__(self, parent, ndevices, routes):
        """ndevices ist die Anzahl verfügbare Netzwerkkarten, routes eine
           Liste von Route-Objekten."""
        gridlib.Grid.__init__(self, parent, -1)
        self.moveTo = None
        self.table = RoutingDataTable(ndevices)
        self.SetTable(self.table, True)

        self.importRoutes(routes)

        self.labelcontext = m = wx.Menu()
        self.delrow = None
        rmroute = m.Append(wx.NewId(), "Route &entfernen")

        self.Bind(wx.EVT_MENU, self.OnDeleteRoute, rmroute)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)

        # Die folgende Zeile darf unter Windows nicht ausgeführt werden
        #self.CreateGrid(10, 5)
        self.SetRowLabelSize(25)

        for i, size in ((0, 115), (1, 115), (2, 115), (3,55), (4, 50)):
            self.SetColSize(i, size)

    def importRoutes(self, routes):
        """Nimmt die Daten aus einer Liste von Route-Objekten und
           legt sie im Grid ab."""

        # Wir unterstützen nicht beliebig lange Routingtabellen!
        n = min(len(routes), self.GetNumberRows())
        
        for row in range(n):
            self.SetCellValue(row, 0, routes[row].dest)
            self.SetCellValue(row, 1, routes[row].netmask)
            if routes[row].gw == None:
                self.SetCellValue(row, 2, '')
            else:
                self.SetCellValue(row, 2, routes[row].gw)
            self.SetCellValue(row, 3, str(routes[row].metric))
            self.SetCellValue(row, 4, str(routes[row].link+1))

    def isValidRoute(self, row):
        """Überprüft, ob Zeile row eine gültige Route darstellt, und liefert
           entsprechend True oder False."""
        
        try:            
            for i in range(2):
                val = routing.binaryIP(self.GetCellValue(row, i))
                gw = self.GetCellValue(3,i)
            if gw != '' and not routing.isValidIP(gw):
                raise ValueError
            metric = int(self.GetCellValue(row, 3))
            device = int(self.GetCellValue(row, 4))
            return True
        except ValueError:
            return False

    def exportRoutes(self):
        """Gibt eine Liste von Route-Objekten zurück"""

        routes = [] 

        for row in range(self.GetNumberRows()):
            if self.isValidRoute(row):
                gw = self.GetCellValue(row, 2)
                if gw == '':
                    gw = None
                routes.append(routing.Route(self.GetCellValue(row, 0),
                                            self.GetCellValue(row, 1),
                                            gw,
                                            int(self.GetCellValue(row, 3)),
                                            int(self.GetCellValue(row, 4))-1))
        routing.sortRoutes(routes)
        return routes

    def OnCellChange(self, evt):

        row, col = evt.GetRow(), evt.GetCol()        
        value = self.GetCellValue(row, col)

        if col >= 3 or (col == 2 and value == '') or routing.isValidIP(value):
            self.SetCellBackgroundColour(row, col, wx.WHITE)
        else:
            self.SetCellBackgroundColour(row, col, wx.RED)
            self.moveTo = (row, col)

    def OnIdle(self, event):
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None
        event.Skip()

    def OnLabelRightClick(self, event):
        row, col = event.GetRow(), event.GetCol()
        # Wir sind nur an Klicks auf die Zeilenlabels interessiert
        if row < 0: 
            return
        self.delrow = row
        self.PopupMenu(self.labelcontext)
    
    def OnDeleteRoute(self, event):
        if self.delrow != None:
            self.DeleteRows(self.delrow, 1)
            self.delrow = None


class AutoWidthListCtrl(wx.ListCtrl, 
                        listmix.ListCtrlAutoWidthMixin,
                        listmix.TextEditMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize,style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)


class ARPCachePanel(wx.Panel):
    def __init__(self, parent, arpcache):
        wx.Panel.__init__(self, parent, -1)

        tID = wx.NewId()

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.il = wx.ImageList(16,16)
        self.idx1 = 0

        self.list = AutoWidthListCtrl(self, tID, size=(300,100),style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)
        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.list, 1, wx.EXPAND)

        self.PopulateList(arpcache)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def PopulateList(self, data):
        self.list.InsertColumn(0, 'IP-Adresse')
        self.list.InsertColumn(1, 'MAC-Adresse')
    
        index = 0
        for key, data in data.items():
            self.list.InsertImageStringItem(index, key, self.idx1)
            self.list.SetStringItem(index, 1, data)
            index += 1
       
        self.list.SetColumnWidth(0, 140)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def exportList(self):
        cache = {}
        n = self.list.GetItemCount()
        for index in range(n):
            ip = self.list.GetItem(index, 0).GetText()
            mac = self.list.GetItem(index, 1).GetText()
            if routing.isValidIP(ip):
                cache[ip] = mac
        return cache

            
class ARPCacheDialog(wx.Dialog):
    def __init__(self, parent, node):        
        wx.Dialog.__init__(self, parent, -1, "ARP Cache", size=(300,500))

        self.node = node
        
        self.listpanel = ARPCachePanel(self, node.model.arpcache)
        
        border, ok, cancel = addOKCancel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.listpanel, 0, wx.EXPAND)
        box.Add(border, 0, wx.EXPAND)

        self.SetSizer(box)
        box.Fit(self)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnOK, ok)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel)

    def OnOK(self, event):
        self.node.model.arpcache = self.listpanel.exportList()
        event.Skip()
    
    def OnCancel(self, event):
        event.Skip()
        

class SwitchPortAssignmentPanel(wx.Panel):
    def __init__(self, parent, node, portassignment):
        wx.Panel.__init__(self, parent, -1)

        tID = wx.NewId()

        self.node = node
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.il = wx.ImageList(16,16)
        self.idx1 = 0

        self.list = AutoWidthListCtrl(self, tID, size=(200,100),style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)
        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.list, 1, wx.EXPAND)

        self.PopulateList(portassignment)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def PopulateList(self, data):
        self.list.InsertColumn(0, 'MAC-Adresse')
        self.list.InsertColumn(1, 'Port')
    
        index = 0
        for key, data in data.items():
            self.list.InsertImageStringItem(index, key, self.idx1)
            port = str(self._findPortNr(data))            
            self.list.SetStringItem(index, 1, port)
            index += 1
        
        self.list.SetColumnWidth(0, 150)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)


    def _findPortNr(self, dest):
        portnr = 0
        for edge in self.node.edges:            
            print edge.origin(), edge.destination()
            portnr += 1
            if edge.oppositeTo(self.node) == dest:
                return portnr
        raise ValueError("Gesuchter Knoten ist nicht in meiner Kantenliste")

    def exportList(self):
        cache = {}
        n = self.list.GetItemCount()
        nports = len(self.node.edges)
        for index in range(n):
            mac = self.list.GetItem(index, 0).GetText()
            try:
                port = int(self.list.GetItem(index, 1).GetText())
                if port > 0 and port <= nports:
                    cache[mac] = self.node.edges[port-1].oppositeTo(self.node)
            except ValueError:
                pass
        return cache


class SwitchPortAssignmentDialog(wx.Dialog):
    def __init__(self, parent, node):        
        wx.Dialog.__init__(self, parent, -1, "Ports", size=(200,500))

        self.node = node
        
        self.listpanel = SwitchPortAssignmentPanel(self, node, node.model.mactable)
        
        border, ok, cancel = addOKCancel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.listpanel, 0, wx.EXPAND)
        box.Add(border, 0, wx.EXPAND)

        self.SetSizer(box)
        box.Fit(self)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnOK, ok)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel)

    def OnOK(self, event):
        self.node.model.mactable = self.listpanel.exportList()
        event.Skip()
    
    def OnCancel(self, event):
        event.Skip()




class GraphFrame(wx.Frame):
    def __init__(self, title='Graph Frame', parent=None):
        super(GraphFrame, self).__init__(parent, title=title,
            size=(800,600),
            style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.gw = wxgraph.GraphWindow(self)
    def addNode(self, node):
        return self.gw.addNode(node)
    def addEdge(self, edge):
        return self.gw.addEdge(edge)
    def addTraveller(self, traveller):
        self.gw.addTraveller(traveller)
   
def onSendARPRequest(node):
    """User-Interface zum Verschicken eines ARP-Request von node aus."""
    global frame

    if not isinstance(node, devices.Router):
        return

    dlg = wx.TextEntryDialog(frame, "Welche IP-Adresse soll gefunden werden?", 'IP-Adresse eingeben', '')
    if dlg.ShowModal() == wx.ID_OK:
        ipaddr = dlg.GetValue()

        try:
            request = generateARPRequest(node, ipaddr)
            node.parent.addTraveller(request)
        except ValueError:
            err = wx.MessageDialog(frame, 'Diese IP-Adresse ist nicht mittels ARP erreichbar. Entweder fehlt eine Route zu einem lokalen Netz oder die IP-Adresse ist nicht in einem lokalen Netz.', 'IP-Adresse nicht erreichbar', wx.OK | wx.ICON_ERROR)
            err.ShowModal()
            err.Destroy()

    dlg.Destroy()
   

def generateARPRequest(node, ipaddr):

        routes = routing.routesTo(node.model.routes, ipaddr)
        for route in routes:
            # Wir können nur Routen verwenden, die keinen Gateway gesetzt 
            # haben, d.h. Routen für lokale Netze
            if route.gw == None:
                device = node.connectors[route.link]
                print "ARP Request: Verwendetes Netz: ", route.dest, " MAC", device.mac
                return devices.ARPRequest(device, node.getOppositeTo(device), device.mac, node.model.devs[route.link], ipaddr)

        raise ValueError("IP-Adresse mittels ARP nicht erreichbar")
   

def onSendIPPacket(node):
    global frame

    if not isinstance(node, devices.Router):
        return

    dlg = wx.TextEntryDialog(frame, "An welche IP-Adresse soll das Paket geschickt werden?", 'IP-Adresse eingeben', '')
    if dlg.ShowModal() == wx.ID_OK:
        ipaddr = dlg.GetValue()
        packet = devices.IPPacket(None, ipaddr, "Hallo Welt")
        node.handleIPPacket(packet)
        
    dlg.Destroy()
    
def onViewARPCache(node):
    global frame

    dialog = ARPCacheDialog(frame, node)
    dialog.Show(True)

def onViewMACTable(node):
    global frame
    dialog = SwitchPortAssignmentDialog(frame, node)
    dialog.Show(True)


def onEditRoutingTable(node):
    global frame

    dialog = RoutingTableDialog(frame, node)
    dialog.Show(True)

  


def buildgraph(frame, nodes, packets):
    """Hilfsfunktion, welche aus nodes und packets einen Graphen baut."""
    for node in nodes:
        frame.addNode(node)

    for node in nodes:
        for edge in node:
            frame.addEdge(edge)

    for packet in packets:
        frame.addTraveller(packet)
    

def wxinit():
    app = wx.App()
    return app
   
def init(nodes, packets, application = None):
    """Baut einen manipulierbaren Graphen aus nodes, verschickt packets und
       startet die wxPython mainloop."""
    global frame
    if not application:
        application = wxinit()
    frame = GraphFrame('Netzwerk-Simulator')
    buildgraph(frame, nodes, packets)
    frame.Show()
    application.MainLoop()


def runthreaded(nodes, packets, application = None):
    """Funktioniert unter Windows höchstwahrscheinlich nicht, unter Linux
       jedoch sehr zuverlässig."""
    thread.start_new_thread(init, (nodes, packets, application))
