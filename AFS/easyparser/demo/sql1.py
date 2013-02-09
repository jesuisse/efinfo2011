import sys
sys.path.append("../../easyparser")
from easyparser import *


def literal2Token(literal):
   if literal in ['SELECT', 'FROM', 'WHERE', '=', ',']:
      return (literal.lower(), literal)
   elif literal[0] == "'" and literal[-1] == "'":
      return ('string', literal[1:-1])
   elif literal[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
      return ('number', int(literal))
   else:
      return ('name', literal)

eingabe = raw_input("Abfrage: ")
literals = eingabe.split(" ")
for literal in literals:
   print literal2Token(literal) 


