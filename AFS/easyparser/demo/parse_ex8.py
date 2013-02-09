import sys
sys.path.insert(0, "../easyparser")
from recursivedescent import Terminal, Nonterminal, Action, RecursiveDescentParser

s = Nonterminal("Satz")
dart = Nonterminal("Bestimmter Artikel")
uart = Nonterminal("Unbestimmter Artikel")
perspron = Nonterminal("Personalpronomen")
posspron = Nonterminal("Possesivpronomen")
praep = Nonterminal("Praeposition")
nn = Nonterminal("Nomen")
np = Nonterminal("Nominalphrase")
vp = Nonterminal("Verbphrase")
pp = Nonterminal("Praepositionalphrase")
vtr = Nonterminal("Transitives Verb")
adj = Nonterminal("Adjektiv")
name = Nonterminal("Name")

stop = Nonterminal("Quit")

EOL = Terminal("EOL")

# Bruno geht mit Gina in die Klasse. Er mag sie.       -> Bruno mag Gina
# Gina kennt Bruno. Ich gehe mit ihr in die Klasse. Ich mag sie nicht.  -> Ich mag Gina nicht
# Gina geht in meine Klasse. Sie ist nett. -> Ich mag Gina

s >> np + vtr + np + EOL | np + vtr + pp + EOL | np + vtr + np + pp + EOL | np + vtr + pp + pp + EOL | np + vtr + adj + EOL
np >> dart + nn | dart + adj + nn | perspron | name | posspron + nn
pp >> praep + np 
vtr >> Terminal('ist') | Terminal('mag') | Terminal("gehe") | Terminal("geht") | Terminal('hasse') | Terminal('hasst') | Terminal('kenne') | Terminal('kennt')
dart >> Terminal("der") | Terminal("die") | Terminal("das") | Terminal("ein") | Terminal("eine")
uart >> Terminal("ein") | Terminal("eine") | Terminal("einen")
nn >> Terminal("sport-club") | Terminal("klasse")
name >> Terminal("gina") | Terminal("lisa") | Terminal("bruno")
adj >> Terminal("gleich") | Terminal("gleiche") | Terminal("doof") | Terminal("doofe") | Terminal("nett") | Terminal("nette")
perspron >> Terminal("ich") | Terminal("sie") | Terminal("er") | Terminal("ihn") | Terminal('ihm') | Terminal('ihr') | Terminal('mich')
posspron >> Terminal("meine") | Terminal("meinen") | Terminal("seine") | Terminal("seinen")
praep >> Terminal("mit") | Terminal("in")


maleReferent = None
femaleReferent = None


def nn_action(nomen):
    return ('nn', nomen)

def adj_action(adj):
    if adj == 'doof':
        return ('adj', 'negativ')
    elif adj == 'nett':
        return ('adj', 'positiv')
    else:
        return ('adj', None)
    

def vtr_action(verb):
    if verb == 'mag':
        return 'mag'
    else:
        return verb
    
def perspron_action(pron):
    if pron == 'ich':
        return ('pron',  None)
    elif pron == 'mich':
        return ('pron', None)
    elif pron == 'er':
        return ('pron', 'm')
    elif pron == 'ihn':
        return ('pron', 'm')
    elif pron == 'ihm':
        return ('pron', 'm')
    elif pron == 'ihr':
        return ('pron', 'f')
    elif pron == 'sie':
        return ('pron', 'f')

def name_action(name):
    
    if name == 'gina' or name == 'lisa':
        return ('name', name, 'f')
    else:
        return ('name', name, 'm')

def np_action(*args):
    if len(args) == 1:
        return args[0]
    else:
        return args[-1]

def pp_action(praep, np):
    return np
        
def s_action(*args):
    subj = args[0]
    verb = args[1]

    setReferent(subj)
    subj = extractName(subj)
        
    if verb == 'ist':
        if args[2][0] == 'adj':
            return ('ich', subj, args[2][1])
    
    if verb == 'mag':
        setReferent(args[2])
        return (subj, extractName(args[2]), 'positiv')

    if verb == 'hasse' or verb == 'hasst':
        setReferent(args[2])
        return (subj, extractName(args[2]), 'negativ')

    for arg in args[2:]:
        setReferent(arg)
    

def setReferent(semantic):
    global maleReferent, femaleReferent
    if semantic[0] == 'name':
        if semantic[2] == 'm':
            maleReferent = semantic[1]
            print "Referent ist jetzt", maleReferent
        if semantic[2] == 'f':
            femaleReferent = semantic[1]
            print "Referetin ist jetzt", femaleReferent
        

def extractName(semantic):
    if semantic[0] == 'name':
        return semantic[1]

    if semantic[0] == 'pron':
        if semantic[1] == 'f':
            return femaleReferent
        elif semantic[1] == 'm':
            return maleReferent
        else:
            return 'ich'


p = RecursiveDescentParser(s)

p.setParseAction(name, name_action)
p.setParseAction(perspron, perspron_action)
p.setParseAction(vtr, vtr_action)
p.setParseAction(adj, adj_action)
p.setParseAction(nn, nn_action)
p.setParseAction(np, np_action)
p.setParseAction(pp, pp_action)
p.setParseAction(s, s_action)


while True:
    src = raw_input("Gib etwas ein: ")
    src = src.lower()
    tokens = src.split(" ")
    tokens.append("EOL")
    g = p.parse(tokens)
    try:
        semantic = g.next()
        print "Aha, ich verstehe:"
        print semantic        
    except StopIteration:
        print "Das verstehe ich leider nicht."
    
        








