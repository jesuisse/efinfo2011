import pprint

from recursivedescent import Terminal, Nonterminal, Action, RecursiveDescentParser

s = Nonterminal("Satz")
ausdruck = Nonterminal("Ausdruck")
term = Nonterminal("Term")
faktor = Nonterminal("Faktor")
zahl = Nonterminal("Zahl")

# Definiert eine Grammatik, welche Ausdrücke wie 3 * 4 + 2 oder 3 * (4 + 2)
# beschreibt.

s >> ausdruck + Terminal("?")
ausdruck >> term | ausdruck + Terminal("+") + term | ausdruck + Terminal('-') + term 
term >> faktor | faktor + Terminal("*") + term | faktor + Terminal("/") + term
faktor >> zahl | Terminal('(') + ausdruck + Terminal(')')
zahl >> Terminal('1') | Terminal('2') | Terminal('3') | Terminal('4')

p = RecursiveDescentParser(s)

while True:
    src = raw_input("Gib etwas ein: ")
    src = src.lower()
    tokens = src.split(" ")
    g = p.parse(tokens)
    try:
        semantic = g.next()
        print "Aha, ich verstehe:"
        pprint.pprint(semantic, indent=2)
        print
    except StopIteration:
        print "Das verstehe ich nicht."

        








