"""
Implements a recursive descent parser with some improvements to increase
it's speed.

Define your grammar like this, taking care to avoid left-recursion (left
recursion will send the parser into a recursive loop):

np = Nonterminal("Noun Phrase")
det = Nonterminal("Determiner")
adj = Nonterminal("Adjective")
adjlist = Nonterminal("List of adjectives")
nn = Nonterminal("Noun")

np >> det + nn | det + adjlist + nn
adjlist >> adj | adj + adjlist
adj >> Terminal("tall") | Terminal("tiny")
det >> Terminal("a") | Terminal("the")
nn >> Terminal("dwarf") | Terminal("giant") | Terminal("boy")

Note how the recursive part of adjlist is defined as adj + adjlist instead
of the left-recursive adjlist + adj!

You may also use multiple >> to specify additional alternative expansions:

nn >> Terminal("dwarf")
nn >> Terminal("giant")
nn >> Terminal("boy")

"""

__author__ = "Pascal Schuppli <pschuppli@phar.ch>"
__version__ = 1.0

class GrammarAccumulator(object):
    """The GrammarAccumulator is used to store individual elements of a
       grammar while constructing it. There are basically two operators
       for grammars: + and |, with + building sequences of tokens to match
       and | for alternatives, with + having the higher precedence.

       Every token sequence is pushed on a stack. Sequences are represented
       using lists, so every stack entry consists of token sequence lists.

       Whenever we encounter a |, a new empty active sequence list is created
       and pushed on the stack.

       IMPORTANT: If you're building a grammar and you encounter an object
       of this class, chances are you did something wrong when you defined
       your grammar! Objects of this class are used internally in the
       construction process and shouldn't be exposed to you in a correct
       grammar."""       

    def __init__(self, element, name=None):
        self.name = name        
        self.active = [element]
        self.stack = [self.active]

    def __or__(self, other):

        if issubclass(type(other), basestring):
            other = Terminal(other)
        
        if issubclass(type(other), GrammarAccumulator):
            # If we have Akku | Akku, then we simply extend
            # our own stack with the other's contents (we should
            # actually preprend, but order doesn't matter) and
            # throw away the other GrammarAccumulator.
            self.stack.extend(other.stack)
        else:            
            self.active = [ other ]
            self.stack.append(self.active)
        return self
    
    def __add__(self, other):
        # If this turns out to be possible after all, we will
        # probably have to deal with it by extending self's
        # stack and active list, taking care to join self's
        # and the other's active instead of creating a wrong
        # alternative.
        assert(not issubclass(type(other), GrammarAccumulator))

        if issubclass(type(other), basestring):
            other = Terminal(other)
        
        self.active.append(other)
        return self

    def __str__(self):
        total = []
        for alt in self.stack:
            total.append("+".join(map(lambda x: x.getName() if x != None else "None", alt)))            
        return " | ".join(total)

class BasicGrammarElement(object):
    """This is the base class for Terminals and Nonterminals.
       It overloads the + and | operators. Those are called
       when a terminal or nonterminal is seen on the left side
       of one of these operators.

       When we encounter such a situation, we create a new
       GrammarAccumulator which contains only the element on
       the left side of the operator, and then make sure
       GrammarAccumulator's overloaded operator takes care
       of joining the right operand."""
    def __init__(self, name=None):
        self.name = name
      
    def __or__(self, other):        
        return GrammarAccumulator(self, self.getName()) | other
    
    def __add__(self, other):
        return GrammarAccumulator(self, self.getName()) + other

    def __call__(self, **kwargs):
        return FeaturedElement(self, kwargs)

    def getName(self):
        return self.name

    
class Terminal(BasicGrammarElement):
    """A Terminal is an atomic element of your grammar, meaning
       that it can't expand to a sequence of other Terminals.
       Terminals can often be seen directly in the stream you
       are parsing, but this depends on what your lexer does to
       break your input stream into tokens for the parser.

       You can define and use Terminals like so:

       the = Terminal("the")
       boy = Terminal("boy")
       runs = Terminal("runs")

       sentence = Nonterminal("Sentence")
       sentence >> the + boy + runs  """
    def __init__(self, name):
        """Pass the name of the token as the only argument.

           The name doesn't have to be a string, but if it can
           be converted to a string representation by str(...),
           you will get decent debugging information."""           
        self.name = name
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<T " + str(self) + " >"

    
class Nonterminal(BasicGrammarElement):
    """A Nonterminal is an element of your grammar which can
       be expanded to one or several sequences of Terminals and
       Nonterminals.
       
       Nonterminals are larger 'concepts' represented by several
       tokens of the stream you are parsing. Every grammar has a
       sentence symbol, which is the topmost nonterminal which
       describes the whole of your input stream when it is valid.

       To construct a grammar, you have to explicitely create
       nonterminals:

       det = Nonterminal("Determiner")
       adj = Nonterminal("Adjective")
       nn = Nonterminal("Noun")
       np = Nonterminal("Nounphrase")

       np >> det + adj + nn      

       You can also define recursive grammars:

       adjlist = adj | adj + adjlist
       np2 >> det + nn | det + adjlist + nn """       
    def __init__(self, name, actionFunc=None):
        """Constructs a Nonterminal object. You must provide a
           unique name for all nonterminals."""
        self.name = name
        self.akku = None
        if actionFunc != None:
            self.action = Action(actionFunc)
        else:
            self.action = None

    def getRHS(self):
        return self.akku.stack

    def __rshift__(self, other):       

        if issubclass(type(other), basestring):            
            other = Terminal(other)
        
        if self.akku:
            return self.akku | other
        else:
            if issubclass(type(other), GrammarAccumulator):
               self.akku = other
            else:
                self.akku = GrammarAccumulator(other, other.getName())
            return self.akku

    def __str__(self):
        return self.name + ": " + str(self.akku)

    def __repr__(self):
        return "<NT " + str(self) + " >"


class Action(BasicGrammarElement):
    """A parse action is a function that is called when the parser reaches
       the position in the parse where the action is defined."""
    def __init__(self, function):
        self.function = function

    def run(self, arglist):
        return self.function(*arglist)

    def __str__(self):
        return "<ACTION>"

    def __repr__(self):
        return "<ACT func " + hex(id(self.function)) + "  >"

    def getName(self):
        return str(self)


class FeaturedElement(BasicGrammarElement):
    """A featured Element is a thin wrapper around a Terminal or Nonterminal
       which stores features required by the terminal or nonterminal at this
       position in the grammar."""
    def __init__(self, target, features):
        self.target = target
        self.features = features

    def getName(self):
        return self.target.getName()

    def getRHS(self):        
        return self.target.getRHS()

    def strip(self):
        return self.target
                
    def __str__(self):
        return " ".join(map(lambda x: str(x), self.features))

    def __repr__(self):
        return "<FT t=" + str(self.target) + " feats=" + str(self) + " >"


    
