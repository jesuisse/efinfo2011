# -*- coding: utf-8 -*-

def makeNode(key, value):
    """Erzeugt einen Knoten des Baumes ohne linke und rechte Kinder"""    
    return [key, value, None, None]

def getKey(node):
    return node[0]

def getValue(node):
    return node[1]

def getLeftChild(node):
    return node[2]

def getRightChild(node):
    return node[3]

def setLeftChild(node, child):
    node[2] = child

def setRightChild(node, child):
    node[3] = child


def lookup(node, key):
    """Liefert den Knoten zurück, der den Schlüssel key enthält, oder
       None, wenn kein solcher Schlüssel im Baum gespeichert ist."""

    if node == None:
        return None

    myKey = getKey(node)
        
    if key == myKey:
        return node
    elif key < myKey:
        return lookup(getLeftChild(node), key)
    else:
        return lookup(getRightChild(node), key)

def lookupValue(root, key):
    node = lookup(root, key)
    if node:
        return getValue(node)
    else:
        raise KeyError("Key not available in tree")

def findInsertionLocation(node, key):

    myKey = getKey(node)
        
    if key == myKey:
        raise ValueError("Key already present in tree")        
    elif key < myKey:
        follow = getLeftChild(node)
    else:
        follow = getRightChild(node)

    if follow == None:
        return node
    else:
        return findInsertionLocation(follow, key)
        

def insert(root, key, value):
    """Fügt einen Schlüssel und Wert in den Baum ein"""

    node = findInsertionLocation(root, key)

    nodeKey = getKey(node)

    newNode = makeNode(key, value)

    if key < nodeKey:
        setLeftChild(node, newNode)
    else:
        setRightChild(node, newNode)
 

if __name__ == '__main__':
    root = makeNode(50, "Pascal")
    
    
  
