# -*- coding: utf-8 -*-
"""
Implements a very simple recursive descent parser generator
"""
import random

class GrammarElement(object):
    def __init__(self):
        pass    
    
class Nonterminal(GrammarElement):
    def __init__(self, alternatives = [], name = None):        
        GrammarElement.__init__(self)
        self.alternatives = map(self._wrapInRHS, alternatives)
        self.name = name

    def _wrapInRHS(self, element):
        if issubclass(type(element), (Terminal, Forward, Nonterminal)):
            return RHS([element])
        else:
            return element
        
    def __or__(self, other):
        if issubclass(type(other), (Terminal, Forward, Nonterminal)):
            self.alternatives.append(RHS([other]))
            return self
        elif issubclass(type(other), RHS):
            self.alternatives.append(other)
            return self        
        else:
            raise ValueError("Unknown type " + str(other))

    def __add__(self, other):
        if issubclass(type(other), (Terminal, Nonterminal, Forward)):
            return RHS([self, other])
        elif issubclass(type(other), RHS):
            return other.prepend(self)
        else:
            raise ValueError("Unknown type " + str(other))

    def parse(self, stream):
        original = copyStream(stream)        
        for candidate in self.alternatives:
            streamcopy = copyStream(original)
            print str(self), ": Parsing candidate", str(candidate), "with tokenpos", stream[0], streamcopy[0]
            for theparse in candidate.parse(streamcopy):
                stream[0] = streamcopy[0]
                yield ('NT', theparse)
            stream[0] = original[0]

    def __str__(self):
        if self.name:
            return "{NT "+self.name+"}"
        else:
            return "NT[...]"
        #return "NT[" + " | ".join(map(lambda x: str(x), self.alternatives))

class RHS(object):
    def __init__(self, rhs = []):        
        self.rhs = map(lambda x: self._realizeForwards(x), rhs)

    def _realizeForwards(self, element):
        if issubclass(type(element), Forward) and element.replacement:
            return element.replacement
        else:
            return element
                      
    def prepend(element):
        self.rhs.insert(0, self._realizeForwards(element))
        return self

    def __add__(self, other):
        if issubclass(type(other), (Terminal, Nonterminal, Forward)):
            self.rhs.append(self._realizeForwards(other))
            return self
        elif issubclass(type(other), RHS):
            self.rhs.extend(other.rhs)
            return self
        else:
            raise ValueError("Unknown type " + str(other))

    def __or__(self, other):
        return Nonterminal(alternatives=[self, other])

    def parse(self, stream):
        print "Starting to parse RHS"
        for p in self.parse_rest(stream, 0, []):
            yield p
                
    def parse_rest(self, stream, pos, have):

        # if we're at the end of the right hand side, yield the result
        if pos == len(self.rhs):
            #print "Completed parse of RHS", self.rhs , ": ", have
            yield have
            return

        print "parse RHS rest", self.rhs[pos:], "having", have, "with", currentToken(stream)
        
        # otherwise, for every parse of the current element,
        # yield all parses of the rest of the rhs
        rid = random.randint(1,2000)
        for aparse in self.rhs[pos].parse(stream):
            mycopy = have[:]
            mycopy.append(aparse)            
            print "parse element", mycopy, "in", rid
            for restparse in self.parse_rest(stream, pos+1, mycopy):
                yield restparse

        print "Failed parse of RHS", self.rhs

def __str__(self):
         return "RHS[" + " ".join(map(lambda s: str(s), self.rhs)) + "]"
                
class Terminal(object):
    def __init__(self, name):
        self.name = name        
    
    def __or__(self, other):        
        return Nonterminal(alternatives = [self, other])

    def __add__(self, other):
        if issubclass(type(other), RHS):
            return other.prepend(self)
        else:
            return RHS([self, other])

    def __str__(self):
        return self.name.upper()

    def __repr__(self):
        return "<Terminal " + str(self) + " at " + hex(id(self)) + ">"

    def parse(self, stream):
        tok = currentToken(stream)
        #print "Parsing Terminal", self.name
        if tok == self.name:            
            #print "Success at ", self.name
            stream[0] += 1
            yield ( 'T', self.name )
            return
        #print "Failed at Terminal", self.name, "with token", tok

class Forward(object):
    """Use this if you want to have a recursive definition in your grammar.
       First specify a the recursive element as Forward(), then use << to
       assign to it:
       alist = Forward()
       alist << list + alist """   
    def __init__(self):
        self.replacement = None        

    def __lshift__(self, other):
        self.replacement = Nonterminal(alternatives = [other])

    def __add__(self, other):
        if issubclass(type(other), RHS):
            return other.prepend(self)
        else:
            return RHS([self, other])

    def parse(self, stream):
        if not self.replacement:
            raise ValueError("Forward Definition not realized!")
        return self.replacement.parse(stream)

def normalizeGrammar(grammar):
    if issubclass(type(grammar), (RHS, Forward, Terminal)):
        return Nonterminal([grammar])
    
def parse(grammar, tokengenerator):
    grammar = normalize_grammar(grammar)
    return recursive_descent(grammar, tokengenerator)


def currentToken(stream):
    return stream[1][stream[0]]
 
def copyStream(stream):
    return [stream[0], stream[1]]


det = Terminal("Der") | Terminal("Das") | Terminal("Die")
adj = Terminal("schöne") | Terminal("grosse") | Terminal("braune")
nn = Terminal("Junge") | Terminal("Mädchen")

adjlist = Forward()
adjlist << (adj | (adj + adjlist))
np = det + nn | det + adjlist + nn
vp = Terminal("vp")
s = np + vp

color = Terminal("braune") | Terminal("rote")
test = Terminal("Der") + color + Terminal("Fuchs")

color.name = "name"
adj.name = "adj"
det.name = "det"
nn.name = "nn"
s.name = "s"
adjlist.replacement.name = "adjlist"


g = s.parse([0, ("Das", "schöne", "braune", "grosse", "Mädchen", "vp")])





