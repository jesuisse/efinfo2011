import sys
sys.path.append("../../easyparser")
from easyparser import *

s = Nonterminal('Satz')
np = Nonterminal('Nominalphrase')

s >> np + Terminal('V')
np >> Terminal('ART') + Terminal('NN')

def extractTerminal(token):
   return token[0]

def extractSemantic(token):
   return token[1]

parser = RecursiveDescentParser(s, extractTerminal, extractSemantic)

def np_action(artikel, nomen):
   return nomen

def s_action(np, verb):
   return [np, verb]

parser.setParseAction(s, s_action)
parser.setParseAction(np, np_action)

tokens = [ ('ART', 'Das'), ('NN', 'Krokodil'), ('V', 'schleicht')]
for semantic in parser.parse(tokens):
   print 'Aha, ich verstehe: ', semantic
print 'Keine weiteren Parses.'
