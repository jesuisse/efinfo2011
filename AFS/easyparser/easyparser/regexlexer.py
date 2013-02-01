# -*- coding: utf-8 -*-
"""
regexlexer erstellt einfache lexer (scanner/tokenizer) aus einer Sammlung
von regulären Ausdrücken.

Erstelle einen Lexer, indem du makeLexer mit einer Datenstruktur wie der
folgenden aufrufst:

lexGrammar = [
  '+', '-', '*', '/', '(', ')',
  (' ', r"\s+"),
  ('ZAHL', r"[0-9]+"),
  ('VAR', r"[a-zA-Z][a-zA-Z0-9]*")
]

lexer = makeLexer(lexGrammar)

Anschliessend kannst du einen beliebigen String in tokens zerlegen lassen:

tokens = lexer("2 * (3 + 4)")

"""

import re

def makeLexer(grammar):
    """Creates a simple lexer which uses regular expressions to define
       the tokens it recognizes. Grammar is a list of (token, regex) 
       tuples or simple strings which will represent themselves.
       If a tuple contains None as the token, the recognized element will
       be ignored."""

    compiled = []
    for entry in grammar:
        if isinstance(entry, basestring):
            token = entry
            regex = '\\' + entry
        elif (isinstance(entry, tuple) or isinstance(entry, list)) and len(entry) == 2:
            token, regex = entry            
        else:
            raise ValueError("Token definition entry " + str(entry) + " has wrong format")
        c = re.compile(regex)
        compiled.append((token, c))

    def lexer(string):
        """Takes the input string and tokenizes it, returning a list of
           (token, value) tuples."""
        p = 0
        tokens = []
        while p < len(string):
            for token, regex in compiled:
                match = regex.match(string, p)
                if match != None:
                    p = match.end()
                    if token != None:
                        tokens.append((token, match.group()))
                    break
            else:
                raise ValueError("Unrecognized character '%s' at position %d" % (string[p], p))
               
        return tokens

    return lexer

