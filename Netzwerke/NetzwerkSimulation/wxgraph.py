# -*- coding: utf-8 -*-
'''
This module contains the DoodleWindow class which is a window that you
can do simple drawings upon.
'''

import wxversion
wxversion.ensureMinimal("2.8")
import wx
import math


def getBoundingBox(rects):

    if len(rects) == 0:
        return None
    
    minx = rects[0][0]
    maxx = rects[0][0] + rects[0][2]
    miny = rects[0][1]
    maxy = rects[0][1] + rects[0][3]
    
    for rect in rects:
        minx = min(minx, rect[0])
        maxx = max(maxx, rect[0]+rect[2])
        miny = min(miny, rect[1])
        maxy = max(maxy, rect[1]+rect[3])
        
    return (minx, miny, maxx - minx, maxy-miny)


def addEdge(endpoint1, endpoint2):
    """Fügt eine Kante zwischen node1 und node2 hinzu."""
    return GraphEdge(endpoint1, endpoint2)


class GraphNode(object):
    def __init__(self, x, y, color="orange", model=None, connectors = []):
        """GraphNode-Knostruktor."""
        self.parent = None
        self.radius = 10
        self.strokec = "#333333"
        self.fillcolor = color
        self.model = model
        self.x = x
        self.y = y
        self.edges = []
        self.connectors = connectors[:]
        self.commands = {}

    def __iter__(self):
        """Eine Iteration über eine GraphNode liefert sämtliche mit ihr verbundene Kanten."""
        for edge in self.edges:
            yield edge

    def position(self):
        """Liefert die Position des Knotens als (x,y) Tupel zurück"""
        return (self.x, self.y)

    def setParent(self, parent):
        self.parent = parent

    def setPosition(self, x, y):
        """Setzt die Position dieses Knotens"""
        self.x = x
        self.y = y

    def addConnector(self, connector):
        """Fügt diesem KNoten einen Connector hinzu"""
        self.connectors.append(connector)

    def getConnector(self, index):
        return self.connectors[index]

    def addEdge(self, edge):
        """Fügt diesem Knoten eine Kante hinzu"""
        self.edges.append(edge)

    def getOppositeTo(self, node):
        for edge in self.edges:
            if edge.originatesAt(node) or edge.endsAt(node):
                return edge.oppositeTo(node)
        return None

    def bindCommand(self, id, action):
        """Bindet eine Kommando-Id für Kontextmenüs an eine Aktion."""
        self.commands[id] = action

    def contains(self, pos):
        """Liefert True, wenn der Knoten den Pixel auf Position (x,y) enthält"""
        cx, cy = pos        
        if self.x == None or self.y == None:
            return False
        return (self.x - cx)**2 + (self.y - cy)**2 <= self.radius**2

    def paint(self, gc):
        """Zeichnet die Connectors und den Knoten selbst."""

        # Vielleicht sollten wir ein Flag haben, das bestimmt, ob Connectors unter
        # oder über den eigentlichen Knoten gezeichnet werden?
        self.paintConnectors(gc)
        self.paintNode(gc)

    def paintConnectors(self, gc):
        """Zeichnet die EdgeConnectors dieses Knotens"""
        for connector in self.connectors:
            connector.paint(gc)

    def paintNode(self, gc):
        """Zeichnet den eigentlichen Knoten (ohne Connectors etc.)"""
        gc.SetPen(wx.Pen(self.strokec, 1))
        color = self.fillcolor
        gc.SetBrush(wx.Brush(color))
        gc.DrawEllipse(self.x-self.radius,self.y-self.radius,
                       self.radius*2, self.radius*2)

    def getBoundingBox(self):
        return (self.x-self.radius, self.y-self.radius, 
                self.x+self.radius, self.y+self.radius)


    def onLeftClick(self, event):
        """Wird aufgerufen, wenn auf den Knoten linksgeklickt wird."""
        pass

    def onRightClick(self, event):
        """Wird aufgerufen, wenn auf den Knoten rechtsgecklickt wird."""
        if self.contextmenu:
            self.parent.PopupMenu(self.contextmenu)

    def onContextMenu(self, event):
        cmdid = event.GetId()
        if cmdid in self.commands:
            action = self.commands[cmdid]
            item = self.contextmenu.FindItemById(cmdid)
            action(item)
 
class EdgeConnector(object):
    """Ein EdgeConnector ist Teil einer GraphNode. Jede GraphNode kann über 
       beliebig viele EdgeConnectors verfügen; an jeden EdgeConnector können
       beliebig viele Kanten (GraphEdges) angehängt werden.

       Diese Implementation des EdgeConnectors positioniert den EdgeConnector
       im Zentrum seines Knotens und verfügt über kein eigenes Aussehen."""

    def __init__(self, node):
        self._node = node

    def setNode(self, node):
        self._node = node

    def getNode(self):
        return self._node

    node = property(getNode, setNode, doc = 'Liefert den Mutterknoten dieses Connectors')

    def __iter__(self):
        """Iteriert über den Mutterknoten"""
        for edge in self.node:
            yield edge

    def position(self):
        """Liefert die Position dieses Connectors. Vorgabe ist die Position
           seiner GraphNode."""
        if not self.node:
            return None

        return self.node.position()

    def addEdge(self, edge):
        self.node.addEdge(edge)

    def paint(self, gc):
        """This connector does not have a visual representation, but subclasses
           might have one, so each connector's paint gets called when a node
           is painted."""
        pass
    

class GraphEdge(object):
    def __init__(self, connector1, connector2):
        """Repräsentiert eine gerichtete Kante. Diese verbindet connector1 und 
           connector2 miteinander. Beide können auf None gesetzt werden, wenn 
           sie erst später verbunden werden sollen.

           Connectors können entweder die Knoten selbst oder aber EdgeConnectors
           sein, die einem Knoten zugewiesen sind. Wichtig ist nur, dass sie über
           eine Methode zur Positionsbestimmung (position() -> (x,y)) verfügen."""

        self.connectors = [connector1, connector2]
        self.strokec = "grey"

        for c in self.connectors:
            c.addEdge(self)

    def __iter__(self):
        """Iteriert über die beiden Endpunkte der Kante"""
        yield self.connectors[0]
        yield self.connectors[1]

    def __getitem__(self, item):
        try:
            return self.connectors[item]
        except IndexError:
            raise IndexError("GraphEdge-Objekte verfügen nur über 2 Endpunkt-Elemente!")
         

    def origin(self):
        return self.connectors[0]

    def destination(self):
        return self.connectors[1]

    def _atHelper(self, endpoint, idx):
        if endpoint == self.connectors[idx]:
            return True
        try:
            if endpoint == self.connectors[idx].node:
                return True
        except AttributeError:
            pass
        
        return False

    def originatesAt(self, endpoint):
        return self._atHelper(endpoint, 0)

    def endsAt(self, endpoint):
        return self._atHelper(endpoint, 1)
  
    def oppositeTo(self, base):
        """Liefert den Endpunkt, der base gegenüberliegt. base muss einer der
           Endpunkte dieser Kante sein."""

        if self.originatesAt(base):
            return self.destination()

        if self.endsAt(base):
            return self.origin()

    def paint(self, gc):
        """Zeichnet die Kante, wenn sie an beiden Enden verbunden ist."""
        if all(self.connectors):
            mx1, my1 = self.connectors[0].position()
            mx2, my2 = self.connectors[1].position()
            gc.SetPen(wx.Pen(self.strokec, 1))
            gc.StrokeLine(mx1, my1, mx2, my2)


def distance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

class EdgeTraveller(object):
    """Ein EdgeTraveller ist eine Animation, die von einem Ende
       einer Kante zum anderen läuft. Trifft sie dort ein, wird 
       die onArrival-Funktion mit dem EdgeTraveller als Argument 
       aufgerufen."""
    def __init__(self, edge, name=None, color="green", onArrival=None):
        """Konstruiert einen EdgeTraveller. Das erste Argument kann ein GraphEdge
           oder ein sonstiges iterierbares Objekt sein, das genau 2 Elemente liefert.
           Alle folgenden Argumente sind optional."""

        try:
            count = 0
            for endpoint in edge:
                count += 1
                if count == 1:
                    self.origin = endpoint
                elif count == 2:
                    self.dest = endpoint
                else:
                    raise ValueError("Zuviele Endpunkte (nur 2 erlaubt!)")
        except TypeError:
            raise ValueError("Erstes Argument muss iterierbar sein!")
            
        self.name = name
        self.radius = 4
        self.color = color
        self.doneAction = onArrival
        self.isDone = False
        self.counter = 0
        self.unit = 3
        self.recalculate()
       
        
    def recalculate(self):
        """Berechnet die Position des Travellers neu, und zwar anhand der
           aktuellen Position der beiden Connectors."""
        p = self.origin.position()
        p2 = self.dest.position()
        
        d = distance(p, p2)
        self.max = d

        if self.counter >= self.max:
            self.isDone = True

        if d == 0:
            self.dx = 0
            self.dy = 0
        else:
            self.dx = (p2[0] - p[0]) / d
            self.dy = (p2[1] - p[1]) / d

        self.x = p[0] + self.counter * self.dx
        self.y = p[1] + self.counter * self.dy
        
    def step(self):
        """Bewegt den Traveller ein Stück weiter die Kante entlang in Richtung
           Ziel. Tut nichts, wenn der Traveller das Ziel bereits erreicht hat."""
        if self.isDone:
            return
        
        self.counter = self.counter + self.unit
        # Wir gehen davon aus, dass die Endpunkte der Strecke sich zwischen zwei
        # Aufrufen von step() verschieben können. Deshalb müssen wir sämtliche 
        # relevanten Grössen neu berechnen und nicht nur die (x,y)-Position. Hätten
        # wir eine Möglichkeit, über Endpunkt-Verschiebungen informiert zu werden,
        # könnten wir hier etwas Rechenzeit sparen.
        self.recalculate()

    def position(self):
        """Liefert die aktuelle Position des Travellers als (x,y) Tupel zurück."""
        return (self.x, self.y)

    def paint(self, gc):
        """Zeichnet den Traveller."""
        if not self.isDone:
            mx, my = self.position()
            gc.SetPen(wx.Pen(self.color, 1))
            gc.SetBrush(wx.Brush(self.color))
            gc.DrawEllipse(mx-self.radius,my-self.radius,
                           self.radius*2, self.radius*2)

            if self.name:
                font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD)
                gc.SetFont(font)
                gc.DrawText(self.name, mx+self.radius*1.5, my)
        



class GraphWindow(wx.Window):

    def __init__(self, parent):
        super(GraphWindow, self).__init__(parent,
            style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self.nodes = [ ]
        self.edges = []
        self.travellers = []
        self.bindEvents()
        self.initBuffer()
        self.dragNode = None
        self.timer = wx.Timer(self)
               

        self.timer.Start(75)
        self.SetBackgroundColour('WHITE')
        

    def bindEvents(self):
        for event, handler in [ 
                (wx.EVT_ERASE_BACKGROUND, self.onEraseBackground), 
                (wx.EVT_LEFT_DOWN, self.onLeftDown), # Start drawing
                (wx.EVT_LEFT_UP, self.onLeftUp),     # Stop drawing 
                (wx.EVT_MOTION, self.onMotion),      # Draw
                (wx.EVT_SIZE, self.onSize),          # Prepare for redraw
                (wx.EVT_IDLE, self.onIdle),          # Redraw
                (wx.EVT_PAINT, self.onPaint),        # Refresh
                (wx.EVT_RIGHT_UP, self.onRightClick),  # Right click
                (wx.EVT_MENU, self.onMenu),          # Context menu
                (wx.EVT_TIMER, self.onTimer),
                (wx.EVT_WINDOW_DESTROY, self.cleanup)]:
            self.Bind(event, handler)
       

    def onEraseBackground(self, evt):
        pass

    def initBuffer(self):
        ''' Initialize the bitmap used for buffering the display. '''
        size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width, size.height)
    
        self.repaint()
                       
        self.reInitBuffer = False

    def repaint(self):
        '''Repaints the whole scene'''

        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        gc = wx.GraphicsContext.Create(dc)

        for edge in self.edges:
            edge.paint(gc)

        for node in self.nodes:
            node.paint(gc)

        for traveller in self.travellers:
            # We should recalculate before painting so that we can move
            # a node via a shell command, but the error introduced will
            # be corrected on the next timer event
            traveller.paint(gc)

    def onTimer(self, event):
        completed = []

        # Move all travellers forward
        for traveller in self.travellers:
            traveller.step()
            if traveller.isDone:
                completed.append(traveller)
               
        if len(self.travellers) > 0:
            self.repaint()
            self.RefreshRect(self.GetRect())
            self.Update()

        for traveller in completed:
            self.travellers.remove(traveller)
            if traveller.doneAction:
                traveller.doneAction(traveller)
   

    def findNodeAt(self, pos):
        for node in self.nodes:
            if node.contains(pos):
                return node
        return None
    
    def onLeftDown(self, event):
        ''' Called when the left mouse button is pressed. '''
        self.CaptureMouse()

        mousepos = event.GetPositionTuple()
        self.dragNode = self.findNodeAt(mousepos)
        if self.dragNode:            
            pos = self.dragNode.position()
            self.dragDelta = (pos[0] - mousepos[0], pos[1] - mousepos[1])
            node = self.dragNode
            if hasattr(node.model, "devs"):
                for dev in node.model.devs:
                    print "IP", dev[0], "Maske", dev[1], "MAC", dev[2].mac
                print
               

    def onLeftUp(self, event):
        ''' Called when the left mouse button is released. '''
        if self.HasCapture():
            self.dragNode = None
            self.ReleaseMouse()

    def onRightClick(self, event):
        """We simply pass on the rightclick to the node that was clicked"""
        node = self.findNodeAt(event.GetPositionTuple())
        self.contextnode = node
        if node:
            node.onRightClick(event)

    def onMenu(self, event):
        if self.contextnode and self.contextnode.contextMenuHandler:
            self.contextnode.contextMenuHandler(event)
    
    def onMotion(self, event):
        ''' Called when the mouse is in motion. If the left button is
            dragging then draw a line from the last event position to the
            current one. Save the coordinants for redraws. '''
        if event.Dragging() and event.LeftIsDown() and self.dragNode:
            mousepos = event.GetPositionTuple()
            pos = self.dragNode.position()
            self.dragNode.setPosition(mousepos[0] + self.dragDelta[0], mousepos[1] + self.dragDelta[1])

            for traveller in self.travellers:
                traveller.recalculate()
            
            self.repaint()
            self.RefreshRect(self.GetRect())
            self.Update()
        
            

    def onSize(self, event):
        ''' Called when the window is resized. We set a flag so the idle
            handler will resize the buffer. '''
        self.reInitBuffer = True

    def onIdle(self, event):
        ''' If the size was changed then resize the bitmap used for double
            buffering to match the window size.  We do it in Idle time so
            there is only one refresh after resizing is done, not lots while
            it is happening. '''
        if self.reInitBuffer:
            self.initBuffer()
            self.Refresh(False)

    def onPaint(self, event):
        ''' Called when the window is exposed. '''
        # Create a buffered paint DC.  It will create the real
        # wx.PaintDC and then blit the bitmap to it when dc is
        # deleted.  Since we don't need to draw anything else
        # here that's all there is to it.
        dc = wx.BufferedPaintDC(self, self.buffer)

    def cleanup(self, event):
        pass

    def addNode(self, node):
        self.nodes.append(node)
        node.setParent(self)
        self.repaint()
        self.Refresh(False)
        return node
 
    def addEdge(self, edge):        
        if edge not in self.edges:
            self.edges.append(edge)
            self.repaint()
            self.Refresh(False)
            return edge
        
    def addTraveller(self, traveller):
        self.travellers.append(traveller)


class GraphFrame(wx.Frame):
    def __init__(self, title='Graph Frame', parent=None):
        super(GraphFrame, self).__init__(parent, title=title,
            size=(800,600),
            style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.gw = GraphWindow(self)
    def addNode(self, node):
        return self.gw.addNode(node)
    def addEdge(self, edge):
        return self.gw.addEdge(edge)
    def addTraveller(self, traveller):
        self.gw.addTraveller(traveller)
       

frame = None
def init():
    global frame
    app = wx.App()
    frame = GraphFrame(None)

    n1 = GraphNode(50, 50, model = NodeModel())
    n2 = GraphNode(400, 200, model = NodeModel())
    n3 = GraphNode(250, 350, model = NodeModel())
            
    c1 = EdgeConnector(n1)
    c2 = EdgeConnector(n1)

    frame.addNode(n1)
    frame.addNode(n2)
    frame.addNode(n3)

    edge1 = addEdge(c1, n2)
    edge2 = addEdge(c2, n3)

    frame.addEdge(edge1)
    frame.addEdge(edge2)

    t1 = EdgeTraveller(edge1, "192.168.1.13", "#447799" )
    t2 = EdgeTraveller(edge2, color = "#772233", onArrival = lambda x: None )
    t3 = EdgeTraveller((edge2[1], edge2[0]), "Blublu")

    frame.addTraveller(t1)
    frame.addTraveller(t2)
    frame.addTraveller(t3)    

    frame.Show()
    app.MainLoop()

import thread

def run():
    thread.start_new_thread(init, ())
    
if __name__ == '__main__':
    init()
