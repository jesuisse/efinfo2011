import pprint

from recursivedescent import Terminal, Nonterminal, Action, RecursiveDescentParser

s = Nonterminal("Satz")
ausdruck = Nonterminal("Ausdruck")
term = Nonterminal("Term")
faktor = Nonterminal("Faktor")
zahl = Nonterminal("Zahl")

# Definiert eine Grammatik, welche Ausdrücke wie 3 * 4 + 2 oder 3 * (4 + 2)
# beschreibt.

s >> ausdruck + Terminal("EOL")
ausdruck >> term | ausdruck + Terminal("+") + term | ausdruck + Terminal('-') + term 
term >> faktor | term + Terminal("*") + faktor | term + Terminal("/") + faktor
faktor >> zahl | Terminal('(') + ausdruck + Terminal(')')
zahl >> Terminal('1') | Terminal('2') | Terminal('3') | Terminal('4') 

def zahl_action(zahl):
    return int(zahl[0])

def faktor_action(*args):
    if len(args) == 1:
        # eine einfache zahl
        return args[0]

    # geklammerter ausdruck; semantischer wert ist nur der
    # ausdruck ohne klammern
    return args[1]

def term_action(*args):
    if len(args) == 1:
        # term besteht nur aus faktor
        return args[0]
    
    # term besteht aus faktor, operator und term
    if args[1] == '*':
        return args[0] * args[2]
    elif args[1] == '/':
        return args[0] / args[2]

def ausdruck_action(*args):
    if len(args) == 1:
        # ausdruck besteht nur aus term
        return args[0]

    # ausdruck beteht aus term, operator und ausdruck
    if args[1] == '+':
        return args[0] + args[2]
    elif args[1] == '-':
        return args[0] - args[2]

def satz_action(ausdruck, fragezeichen):
    return ausdruck

p = RecursiveDescentParser(s)

p.setParseAction(s, satz_action)

p.setParseAction(zahl, zahl_action)
p.setParseAction(faktor, faktor_action)
p.setParseAction(term, term_action)
p.setParseAction(ausdruck, ausdruck_action)


while True:
    src = raw_input("Gib etwas ein: ")
    src = src.lower()
    tokens = src.split(" ")
    tokens.append('EOL')
    g = p.parse(tokens)
    try:
        semantic = g.next()
        print "Aha, das ergibt ", 
        pprint.pprint(semantic, indent=2)
        print
    except StopIteration:
        print "Das verstehe ich nicht."

        








