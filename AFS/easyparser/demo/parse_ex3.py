import sys
sys.path.append("../easyparser")

from recursivedescent import Terminal, Nonterminal, RecursiveDescentParser

def s_action(art, nn):
    print "Satz:", art, nn
    return [art, nn]

def art_action(art):
    print "Art:", art
    return art

def nn_action(nn):
    print "NN:", nn
    return nn

# Definition der Nonterminals 
s = Nonterminal("Satz", s_action)
art = Nonterminal("Artikel", art_action)
nn = Nonterminal("Nomen", nn_action)

# Definition der Terminals 
DER = Terminal("der")
DIE = Terminal("die")
DAS = Terminal("das")
HAUS = Terminal("haus")
KIESWEG = Terminal("kiesweg")
ENTE = Terminal("ente")

# Definiert mithilfe von Features eine Grammatik, welche die Satzfragmente
# "Das Haus", "Die Ente" und "Der Kiesweg" erkennen kann, aber nicht
# "Die Haus", "Das Ente" usw.
s >> art(gen='?g') + nn(gen = '?g')
art >> DER(gen='m') | DAS(gen='n') | DIE(gen='f')
nn >> HAUS(gen='n') | KIESWEG(gen='m') | ENTE(gen='f')

# Parser, der die oben definierte Sprache erkennt
p = RecursiveDescentParser(s, lambda t: t["word"], lambda t: t)

while True:
    src = raw_input("Gib etwas ein: ")
    src = src.lower()
    tokens = src.split(" ")
    # verwandelt die Liste von Worten in eine Liste von Dictionaries 
    fttokens = [ {'word': x} for x in tokens ]
    semantic = p.first(fttokens)
    if semantic != None:
        print "Aha, ich verstehe:"
        print semantic
    else:
        print "Das verstehe ich leider nicht."
    
        








