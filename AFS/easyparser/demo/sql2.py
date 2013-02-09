import sys
sys.path.append("../../easyparser")
from easyparser import *


def literal2Token(literal):
   if literal in ['SELECT', 'FROM', 'WHERE', ',', '=']:
      return (literal.lower(), literal)
   elif literal[0] == "'" and literal[-1] == "'":
      return ('string', literal[1:-1])
   elif literal[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
      return ('number', int(literal))
   else:
      return ('name', literal)

def extractTerminal(token):
   return token[0]

def extractSemantic(token):
   return token[1]


s = Nonterminal('SQL')
spalten = Nonterminal('Spalten')
tabellen = Nonterminal('Tabellen')
bedingung = Nonterminal('Bedingung')
T = Terminal

s >> T('select') + spalten + T('from') + tabellen + T('where') + bedingung
spalten  >> T('name') | T('name') + T(',') + spalten
tabellen >> T('name') | T('name') + T(',') + tabellen
bedingung >> T('name') + T('=') + T('string')
bedingung >> T('name') + T('=') + T('number')
bedingung >> T('name') + T('=') + T('name')

parser = RecursiveDescentParser(s, extractTerminal, extractSemantic)

eingabe = raw_input("Abfrage: ")
literals = eingabe.split(" ")
tokens = [ literal2Token(literal) for literal in literals ]
print "Tokens: ", tokens
for semantic in parser.parse(tokens):
   print 'Aha, ich verstehe: ', semantic
print 'Keine weiteren Parses.'
