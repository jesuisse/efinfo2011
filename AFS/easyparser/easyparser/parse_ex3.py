from recursivedescent import Terminal, Nonterminal, Action, RecursiveDescentParser

def s_action(art, nn):
    print "Satz:", art, nn
    return [art, nn]

def art_action(art):
    print "Art:", art
    return art

def nn_action(nn):
    print "NN:", nn
    return nn


s = Nonterminal("Satz", s_action)
art = Nonterminal("Artikel", art_action)
nn = Nonterminal("Nomen", nn_action)

DER = Terminal("der")
DIE = Terminal("die")
DAS = Terminal("das")
HAUS = Terminal("haus")
KIESWEG = Terminal("kiesweg")
ENTE = Terminal("ente")

# Definiert eine Grammatik, welche Sätze wie "Das alte Haus ist ein Ort" oder
# "Der Kiesweg ist ein Ort" parsen kann.
s >> art(gen='?g') + nn(gen = '?g')
art >> DER(gen='m') | DAS(gen='n') | DIE(gen='f')
nn >> HAUS(gen='n') | KIESWEG(gen='m') | ENTE(gen='f')


p = RecursiveDescentParser(s, lambda t: t["word"], lambda t: t)

while True:
    src = raw_input("Gib etwas ein: ")
    src = src.lower()
    tokens = src.split(" ")
    fttokens = [ {'word': x} for x in tokens ]
    g = p.parse(fttokens)
    try:
        semantic = g.next()
        print "Aha, ich verstehe:"
        print semantic
    except StopIteration:
        print "Das verstehe ich leider nicht."
    
        








