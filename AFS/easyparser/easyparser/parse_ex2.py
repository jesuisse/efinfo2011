from recursivedescent import Terminal, Nonterminal, Action, RecursiveDescentParser

s = Nonterminal("Satz")
art = Nonterminal("Artikel")
nn = Nonterminal("Nomen")
np = Nonterminal("Nominalphrase")
vtr = Nonterminal("Transitives Verb")
adj = Nonterminal("Adjektiv")

# Definiert eine Grammatik, welche Sätze wie "Das alte Haus ist ein Ort" oder
# "Der Kiesweg ist ein Ort" parsen kann.
s >> np + vtr + np 
np >> art + nn 
vtr >> Terminal('ist')
art >> Terminal("der") | Terminal("die") | Terminal("das") | Terminal("ein") | Terminal("eine")
nn >> Terminal("haus") | Terminal("kiesweg") | Terminal("raum") | Terminal("ort")

p = RecursiveDescentParser(s)

def s_action(np1, verb, np2):
    if np2 == 'raum':
        np2 = 'ort'
    if verb == 'ist':
        return [np2, np1]
    else:
        raise ValueError("Kann keinen miniprolog-Fakt erzeugen")
    
def vtr_action(verb):
    return verb

def np_action(artikel, nomen):
    return nomen

def nn_action(nomen):
    return nomen

p.setParseAction(np, np_action)
p.setParseAction(nn, nn_action)
p.setParseAction(vtr, vtr_action)
p.setParseAction(s, s_action)

while True:
    src = raw_input("Gib etwas ein: ")
    src = src.lower()
    tokens = src.split(" ")
    g = p.parse(tokens)
    try:
        semantic = g.next()
        print "Aha, ich verstehe:"
        print semantic        
    except StopIteration:
        print "Das verstehe ich leider nicht."
    

