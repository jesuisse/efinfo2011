import sys
sys.path.append("../easyparser")

from recursivedescent import Terminal, Nonterminal, Action, RecursiveDescentParser

s = Nonterminal("Satz")
art = Nonterminal("Artikel")
nn = Nonterminal("Nomen")
np = Nonterminal("Nominalphrase")
vtr = Nonterminal("Transitives Verb")
adj = Nonterminal("Adjektiv")
stop = Nonterminal("Quit")

# Definiert eine Grammatik, welche Sätze wie "Das alte Haus ist ein Ort" oder
# "Der Kiesweg ist ein Ort" parsen kann.
s >> np + vtr + np | stop
np >> art + nn | art + adj + nn
vtr >> Terminal('ist')
stop >> Terminal("quit") | Terminal("exit") | Terminal("ende")
art >> Terminal("der") | Terminal("die") | Terminal("das") | Terminal("ein") | Terminal("eine")
nn >> Terminal("haus") | Terminal("kiesweg") | Terminal("raum") | Terminal("ort")
adj >> Terminal("alte") | Terminal("breite")

p = RecursiveDescentParser(s)

while True:
    src = raw_input("Gib etwas ein: ")
    src = src.lower()
    tokens = src.split(" ")
    g = p.parse(tokens)
    try:
        semantic = g.next()
        print "Aha, ich verstehe:"
        print semantic
        if semantic[0] == 'Satz' and semantic[1][0][0] == 'Quit':
            break                                                 
    except StopIteration:
        print "Das verstehe ich leider nicht."
    
        








