import pprint
import sys

sys.path.append("../easyparser")

from recursivedescent import Terminal, Nonterminal, Action, RecursiveDescentParser
from regexlexer import makeLexer

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
zahl >> Terminal('ZAHL')

def zahl_action(zahl):
    return int(zahl)

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

p = RecursiveDescentParser(s, lambda t: t[0], lambda t: t[1])

p.setParseAction(s, satz_action)

p.setParseAction(zahl, zahl_action)
p.setParseAction(faktor, faktor_action)
p.setParseAction(term, term_action)
p.setParseAction(ausdruck, ausdruck_action)

# Erstellt einen einfachen Lexer
lex = makeLexer(['+','-','*','/','(',')',('ZAHL', r"[0-9]+"), (None, r"\s+")])


while True:
    src = raw_input("Gib etwas ein: ")
    src = src.lower()
    tokens = lex(src)
    print tokens
    tokens.append(('EOL', None))
    g = p.parse(tokens)
    try:
        semantic = g.next()
        print "Aha, das ergibt ", 
        pprint.pprint(semantic, indent=2)
        print
    except StopIteration:
        print "Das verstehe ich nicht."






