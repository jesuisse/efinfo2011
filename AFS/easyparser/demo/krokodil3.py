import sys
sys.path.append("../../easyparser")
from easyparser import *


s = Nonterminal('Satz')
np = Nonterminal('Nominalphrase')
nn = Nonterminal('Nomen')
v = Nonterminal('Verb')
art = Nonterminal('Artikel')

s >> np + v
np >> art + nn
art >> Terminal('Der') | Terminal('Die') | Terminal('Das')
nn >> Terminal('Hund') | Terminal('Schnecke') | Terminal('Krokodil')
v >> Terminal('bellt') | Terminal('schwimmt') | Terminal('schleicht')

parser = RecursiveDescentParser(s)

def np_action(artikel, nomen):
   return nomen

def nn_action(nomen):
   return nomen

def v_action(verb):
   return verb

def s_action(np, verb):
   return [np, verb]

parser.setParseAction(np, np_action)
parser.setParseAction(nn, nn_action)
parser.setParseAction(v, v_action)
parser.setParseAction(s, s_action)


eingabe = raw_input('Gib was ein: ')
terminals = eingabe.split(' ')
for semantic in parser.parse(terminals):
   print 'Aha, ich verstehe: ', semantic
print 'Keine weiteren Parses.'
