# -*- coding: utf-8 -*-
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

def makeColumnDict(spalten):
   """Erstellt ein Dictionary, das zu einem Spaltennamen den Index
      zurückliefert"""
   cdict = {}
   for idx, spalte in enumerate(spalten):
      cdict[spalte] = idx
   return cdict

def check(zeile, index, name, wert):
   """Überprüft, ob der Wert in Spalte name = wert ist"""
   typ, wert = wert[0], wert[1]
   if typ == 'name':
      return zeile[index[name]] == zeile[index[wert]]
   else:
      return zeile[index[name]] == wert

def extractTerminal(token):
   return token[0]

def extractSemantic(token):
   return token[1]

s = Nonterminal('SQL')
spalten = Nonterminal('Spalten')
tabellen = Nonterminal('Tabellen')
bedingung = Nonterminal('Bedingung')
b1 = Nonterminal("b1")
b2 = Nonterminal("b2")
b3 = Nonterminal("b3")
T = Terminal

s >> T('select') + spalten + T('from') + tabellen + T('where') + bedingung
spalten  >> T('name') | T('name') + T(',') + spalten
tabellen >> T('name') | T('name') + T(',') + tabellen
bedingung >> b1 | b2 | b3
b1 >> T('name') + T('=') + T('string')
b2 >> T('name') + T('=') + T('number')
b3 >> T('name') + T('=') + T('name')

def tabellen_action(*args):
   global alletabellen
   if len(args) == 1:      
      return alletabellen[args[0]]
   else:
      raise ValueError("Mehrere Tabellen sind noch nicht eingebaut")

def spalten_action(*args):
   if len(args) == 1:
      return [args[0]]
   elif len(args) == 3:      
      args[2].insert(0, args[0])
      return args[2]
   else:
      assert False

def b1_action(name, op, wert):
   return (name, ('string', wert))

def b2_action(name, op, wert):
   return (name, ('number', wert))

def b3_action(name, op, wert):
   return (name, ('name', wert))

def bedingung_action(b):
   return b

def sql_action(select, spalten, fr, tabellen, where, bedingung):
   tab = tabellen

   names = tab[0]
   index = makeColumnDict(names)
   namesidx = []
   # Finde die Spalten-Indices der zu behaltenden Spalten
   for spalte in spalten:      
      namesidx.append(index[spalte])

   # Erstelle eine neue Tabelle, die nur die gewollten Spalten
   # enthält
   tabkopie = [ spalten ]
   for zeile in tab[1:]:
      if check(zeile, index, bedingung[0], bedingung[1]):
         zeilenkopie = []
         for idx in namesidx:
            zeilenkopie.append(zeile[idx])
         tabkopie.append(zeilenkopie)

   return tabkopie

parser = RecursiveDescentParser(s, extractTerminal, extractSemantic)
parser.setParseAction(tabellen, tabellen_action)
parser.setParseAction(spalten, spalten_action)
parser.setParseAction(b1, b1_action)
parser.setParseAction(b2, b2_action)
parser.setParseAction(b3, b3_action)
parser.setParseAction(bedingung, bedingung_action)
parser.setParseAction(s, sql_action)

personen = [['id', 'vorname', 'nachname', 'alter'],
            [1, 'Bart', 'Simpson', 10],
            [2, 'Lisa', 'Simpson', 8],
            [3, 'Maggie', 'Simpson', 1]]
spielzeug = [['name', 'besitzer'],
             ['Saxophon', 2],
             ['Krusty-Puppe', 1],
             ['Steinschleuder', 1],
             ['Schnuller', 3]]

alletabellen = { 'personen': personen,
             'spielzeug': spielzeug}

eingabe = raw_input("Abfrage: ")
literals = eingabe.split(" ")
tokens = [ literal2Token(literal) for literal in literals ]
for semantic in parser.parse(tokens):
   print 'Aha, ich verstehe: ', semantic
print 'Keine weiteren Parses.'
