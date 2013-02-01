# -*- coding: utf-8 -*-
"""
Ein Recursive Descent Parser parst einen Token-Strom (der aus einfachen
Strings wie z.B. Wörtern oder aber etwas komplizierterem wie z.B. (Typ,
Wort)-Tupeln bestehen kann), indem er den gleichen Token-Strom mit den
Regeln einer gegebenen Grammatik abzuleiten versucht. Die Ausgabe des
Parsers ist der Ableitungsbaum, der den vorgegebenen Token-Strom erzeugt.

Das bedeutet, dass der Parser für jeden Eingabestrom, der gemäss der
Gramamtik valid ist, den richtigen Ableitungsbaum finden kann; allerdings
ist die Zeitkomplexität im schlimmsten Fall exponentiell.

Beispiel:

Grammatik:

S -> A N V | A N V2 ihn
A -> Der | Die | Das
N -> Junge | Mädchen | Krokodil
V -> rennt | geht | grinst | lacht
V2 -> frisst | küsst 

Wenn der Eingabestrom [ 'Das', 'Krokodil', 'grinst'] vorliegt, wird ein
Recursive Descent - Parser aus dem Satzsymbol S zuerst die Produktion A N V
ableiten, dann alle 3 Möglichkeiten für A versuchen und merken, dass nur
die letzte (Das) funktioniert, dann für N Junge und Mädchen verwerfen und
schliesslich für V nach 'rennt' und 'geht' 'grinst' finden. Der Ableitungsbaum
für diesen Satz ist also S -> A N V, A -> Das, N -> Krokodil, V -> grinst. Der
Parser ist aber noch nicht fertig; er springt zurück und überprüft auch noch
die zweite mögliche Produktion von S, S -> S N, und stellt nach dem Ausprobieren
sämtlicher Möglichkeiten von A und N fest, dass es das 'grinst' aus dem
Eingabestrom nicht aus einem Terminal aus V2 herleiten kann. An dieser Stelle
bricht der Parser ab.

Der Vorteil eines Recursive Descent Parsers ist, dass er für ambivalente
Eingabeströme, also solche, für die es mehrere mögliche Ableitungsbäume gibt,
alle möglichen Ableitungen findet. Der Nachteil ist, dass er recht ineffizient
ist und keine linksrekursiven Grammatiken verarbeiten kann.

Eigenschaften dieser Implementation:

 - Produktion der Ableitungsbäume nur auf Verlangen: Der Parser ist mit
   Generatoren programmiert, so dass er nicht bereits zu Beginn alle möglichen
   Ableitungsbäume für einen Eingabestrom sucht. Wenn also eine Ableitung
   ausreicht, sucht der Parser nur die erste.
 - Caching von bereits geparsten Teilbäumen: Wenn der Parser erfolgreich ein
   Nonterminal erkannt hat, cacht er den Teilbaum, so dass er bei einem
   eventuellen Backtracking die gleiche Arbeit nicht nocheinmal machen muss.
 - Features: Siehe unten

Features:

Features sind im Einbau begriffen. Die oben vorgestellte Grammatik hat das
Problem, dass sie auch Sätze wie "Der Mädchen lacht" oder "Die Krokodil grinst"
zulässt.

Eine augmentierte Feature-Grammatik verhindert dies:
S -> A(gen='?g') N(gen='?g') V 
A -> Der(gen='m') | Die(gen='f') | Das(gen='n')
N -> Junge(gen='m') | Mädchen(gen='n') | Krokodil(gen='n')
V -> rennt | geht | grinst | lacht

Die Arbeitsweise: Ein Element auf der rechten Seite einer Produktion kann
durch Features (in Klammern) ergänzt werden. Z.B. wird dem Terminal 'Der'
das Feature 'gen' (genus) mit dem Wert 'm' zugewiesen. Wird das Nonterminal
A erkannt, werden alle Features auf der rechten Seite vereinigt und und das
Ergebnis wird dem semantischen Wert der Reduktion angehängt. Das gleiche
passiert mit N.

Wenn wir nun S -> A N V zu finden versuchen, kommt nach der Reduktion von
"Der" auf A das gen-Feature mit; da in S -> A(gen=?g) N(gen=?g) V  A ebenfalls
ein gen-Feature trägt, wird die Variable ?g an 'm' gebunden. Wenn der Parser
nun 'Mädchen' auf 'N' reduziert, wird die Unifikation von ?g und 'f' fehl-
schlagen, da ?g bereits an 'm' gebunden ist. Der Parser weiss also, dass der
vorliegende Ableitungsbaum nicht gültig ist und er den Strom, der mit
['Der', 'Mädchen'] beginnt, nicht zu einem gültigen S reduzieren können wird,
und bricht ab.

Features werden nur unterstützt, wenn der semantische Wert eines Tokens ein
Dictionary ist, da die Features vom Parser direkt in dieses Dictionary
gespeichert werden. Das hat auch den Vorteil, dass der Eingabestrom bereits
mit Features angereichert sein kann (oder sogar nur aus Featuren bestehen kann):

[ {'word': 'Der', 'tag': 'A', 'gen': 'm' },
  {'word': 'Mädchen', 'tag': 'N', 'gen': 'f' },
  {'word': 'lacht', 'tag': 'V', } ]

Das ist ein Eingabestrom, der nur aus Featuren besteht und den Satz
"Das Mächdchen lacht" repräsentiert, bereits angereichert mit Informationen
zum Genus und der Wortklasse der einzelnen Wörter. Der Parser kann damit
umgehen, wenn ihm folgende terminalExtractor- und valueExtractor-Funktionen
bei der Konstruktion mitgegeben werden:

def terminalExtractor(token):
   return token['tag']

def valueExtractor(token):
   return token

Die Grammatik kann nun auf massiv gekürzt werden (auf eine einzige Zeile):

S -> A(gen='?g') N(gen='?g') V

       A Feature is something you can attach to a Terminal or Nonterminal.
       When that terminal or nonterminal is recognized and the feature is
       not already bound to a value, the feature extractor is run on its
       semantic value. If the feature is already bound, then the value
       retrieved from the token by the feature extractor is compared to the
       bound value and if they do not agree, a FeatureMismatch exception is
       thrown, which the parser should catch and use to fail the current
       parse.


"""
from grammar import Nonterminal, Terminal, Action, FeaturedElement
from features import Feature
        
class RecursiveDescentParser(object):
    """The Recursive Descent Parser parses a stream of tokens by expanding
       the grammar's sentence symbol according to the grammar productions
       until the expanded stream of terminals matches the input tokens. It
       then returns the parse tree.

       If there are multiple possible parses of your sentence, the parser
       will find them all.

       Be aware this recursive descent parser is slow because it basically
       guesses expansions one after the other, backtracking when it encounters
       a deadend. It does cache nonterminals it has successfully parsed.

       We could improve this by caching RHS parts instead of nonterminals,
       but this is conceptually harder to understand and implement correctly
       with the given recursive implementation (for me)."""

    def __init__(self, sentenceSymbol, terminalExtractor = None, valueExtractor = None, **kwargs):
        """Creates a recursive descent parser from the sentence symbol
           of a grammar. sentenceSymbol is the topmost nonterminal in
           your grammar's hierarchy of nonterminals.

           You can specify two extractor functions which are expected to take
           a token from your tokenstream as their only input and return the
           name of the terminal represented by the token and the semantic value
           of the token, respectively. If you don't pass those extractors, the
           standard extractor will be used which simply uses the token as is
           for both the name and the semantic value."""

        if not issubclass(type(sentenceSymbol), Nonterminal):
            raise TypeError("Expected sentenceSymbol to be of type Nonterminal, but got " + str(type(sentenceSymbol)))
        
        self.grammar = sentenceSymbol
        self._ntmap = {}
        self._ntactions = {}
        self._firstset = {}
        self._tokenmap = {}
        self._actions = {}
        self._parseCache = {}
        self._cacheHits = 0
        self._nonterminals = []
        self._rhs = []

        if terminalExtractor == None:
            self.terminalExtractor = lambda terminal: terminal
        elif callable(terminalExtractor):
            self.terminalExtractor = terminalExtractor
        else:
            raise TypeError("terminalExtractor must be callable!")

        if valueExtractor == None:
            self.valueExtractor = lambda terminal: terminal
        elif callable(valueExtractor):
            self.valueExtractor = valueExtractor
        else:
            raise TypeError("Semantic Value Extractor must be callable!")

        self.setupGrammarRepresentation()

        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            self.debug = False

        # Just for debugging
        self.nonterminals = self._nonterminals
        self.rhs = self._rhs
              
    def cacheInfo(self):
        """Just for debugging"""
        return (self._cacheHits, self._parseCache)
    

    def setupGrammarRepresentation(self):
        """Sets up the internal representation of the grammar.

           All nonterminals are assigned a unique id starting at 0; a
           nonterminal's right-hand sides (rhs) can be found by using
           the nonterminal's id as an index into self._nonterminals.

           The right hand sides of nonterminals are stored in self._rhs;
           so the list of numbers stored in the appropriate self._nonterminals
           is a list of indices into the self._rhs array.

           This gives each nonterminal and each right hand side a unique
           integer id, which makes it easier to implement caching."""
        self._ntmap = {}
        ntid = -1
        agenda = [ self.grammar]
        while agenda:
            current = agenda.pop()
            if issubclass(type(current), FeaturedElement):
                current = current.target
            ntid += 1
            self._nonterminals.append(current.getRHS()[:])

            if current.action != None:
                self._ntactions[ntid] = current.action
                        
            for idx, rhs in enumerate(current.getRHS()):
                
                self._rhs.append(rhs)
                key = len(self._rhs)
                self._nonterminals[ntid][idx] = key-1                
                self._ntmap[current] = ntid 
                for element in rhs:
                    try:
                        element = element.strip()
                    except:
                        pass
                    if issubclass(type(element), Nonterminal) and element not in self._ntmap:
                        agenda.append(element)

    def nonterminalsMap(self):
        """Returns a dictionary keyed by all nonterminals in the grammar
           which maps a nonterminal object to it's integer id."""
        return self._ntmap
    
    def firstSet(self, element):
        """Returns the first set of an element (terminal or nonterminal).

           The first set of a nonterminal is the set of all tokens which
           can start a token sequence produced by expanding this nonterminal.
           The first set of a terminal is the set containing the terminal."""
        if element == None:
            return set((None,))

        # Remove FeaturedElement decorator
        if issubclass(type(element), FeaturedElement):
            key = element
            element = element.target
        else:
            key = element

        
        if key in self._firstset:
            return self._firstset[key]

        firstset = set()

        # Terminals have a firstset containing just themselves
        if issubclass(type(element), Terminal):
            firstset.add(element.getName())
            self._firstset[key] = firstset
            return firstset    
        
        # The firstsets of nonterminals can be found recursively by
        # building the union of the first elements of all right hand
        # sides.        
        for expansion in element.getRHS():
            # This is necessary because some of the nonterminals on the rhs
            # might expand to None (Epsilon / Empty)
            for first in expansion:
                if first == element:
                    # We are doing this right now, don't recurse on it!
                    continue                
                firstset.update(self.firstSet(first))
                if None not in self.firstSet(first):
                    break
           
        self._firstset[key] = firstset
        return firstset

    def candidateExpansions(self, ntid):
        """Creates a dictionary indexed by terminals which will yield
           a list of possible expansions for nonterminal with id ntid"""
        if ntid in self._tokenmap:
            # Get candidates from cache if possible
            return self._tokenmap[ntid]
        
        candidates = {}        
        for rhsid in self._nonterminals[ntid]:
            rhs = self._rhs[rhsid]
            terminals = set()
            for first in rhs:
                terminals.update(self.firstSet(first))
                if None not in self.firstSet(first):
                    break
            for terminal in terminals:
                if terminal == None:
                    if None in candidates:
                        candidates[None].append(rhsid)
                    else:
                        candidates[None] = [ rhsid ]                    
                elif terminal in candidates:
                    candidates[terminal].append(rhsid)
                else:
                    candidates[terminal] = [ rhsid ]

        self._tokenmap[ntid] = candidates
        return candidates

    def clearParseCache(self):
        """Clears the cache of parsed RHS parts"""
        self._parseCache = {}
        self._cacheHits = 0

    def addToCache(self, key, pos, parseResult):
        if key in self._parseCache:
            self._parseCache[key].append((pos, parseResult))
        else:
            self._parseCache[key] = [ (pos, parseResult) ]

    def setParseAction(self, nonterminal, function):
        ntid = self.nonterminalsMap()[nonterminal]
        self._ntactions[ntid] = Action(function)
                                                 
    def parse(self, tokenStream):
        """Parses a sequence of tokens"""
        
        self.clearParseCache()
        return self.parseNonterminal(self.grammar, [0, tokenStream])

    def parseEmpty(self, element, tokenStream):        
        yield None

    def parseAction(self, element, tokenStream, semanticValues):
        # Run the parse action and 
        yield element.run(semanticValues)
        
    def parseNonterminal(self, nonterminal, stream):
        """ A Problem: Currently, FeaturedElements are parsed in parseRestOfRHS
            and that should work. However, once we have the complete set of
            semantic values, how do we construct the Feature semantic value
            for the nonterminal? We should make sure the nonterminal feature?
            do we unify with 'theparse'? """
            
        original = self.copyStream(stream)

        if issubclass(type(nonterminal), FeaturedElement):
            nonterminal = nonterminal.current
            
        ntid = self.nonterminalsMap()[nonterminal]
        
        # We check if there is an earlier parse of this nonterminal
        # at this position in the token stream and return all the
        # results of that parse from the cache
        cachekey = (ntid, stream[0])
        if cachekey in self._parseCache:
            self._cacheHits +=1            
            for pos, result in self._parseCache[cachekey]:
                stream[0] = pos
                yield result
            return
                
        terminalmap = self.candidateExpansions(ntid)
        tokens = [ self.terminalExtractor(self.currentToken(stream)) ]
        if None in self.firstSet(nonterminal):
            tokens.append(None)    

        for tok in tokens:
            if tok not in terminalmap:
                # This prunes this branch because we won't even try to
                # parse candidates 
                continue

            if self.debug:    
                print "Parsing ", str(nonterminal), "with ", tok
                        
            for rhsid in terminalmap[tok]:            
                streamcopy = self.copyStream(original)
                for theparse in self.parseRHS(rhsid, streamcopy):
                    stream[0] = streamcopy[0]
                    if ntid in self._ntactions:
                        result = self._ntactions[ntid].run(theparse)
                    else:
                        result = (nonterminal.getName(), theparse)
                    self.addToCache(cachekey, stream[0], result)
                    yield result
                stream[0] = original[0]

    def parseRHS(self, rhsid, stream):
        for p in self.parseRestOfRHS(rhsid, 0, stream[0], stream, []):
            yield p
    
    def parseRestOfRHS(self, rhsid, pos, streamstart, stream, have):

        if self.debug:
            cachekey = (rhsid, pos, streamstart)        
            print "Parsing RHS Rest with", cachekey
        
        rhs = self._rhs[rhsid]
        if pos == len(rhs):        
            yield have
            return

        element = rhs[pos]
        
        if element == None:            
            parser = self.parseEmpty
        elif issubclass(type(element), Terminal):            
            parser = self.parseTerminal
        elif issubclass(type(element), Action):
            parser = lambda x, y: self.parseAction(x, y, have)
        elif issubclass(type(element), Nonterminal):
            parser = self.parseNonterminal
        elif issubclass(type(element), FeaturedElement):
            parser = self.parseFeaturedElement
        else:
            raise TypeError("Unknown Element Type " + str(type(element)) + " at RHS " + str(rhsid))

        for aparse in parser(element, stream):
            mycopy = have[:]
            mycopy.append(aparse)
            for restparse in self.parseRestOfRHS(rhsid, pos+1, streamstart, stream, mycopy):
                yield restparse

    def parseFeaturedElement(self, element, stream):
        """Parses an Element (Terminal or Nonterminal) with attached features.
           We do this by first doing a normal parse of the target element and
           then trying to unify it's semantic value with the attached features.
           If they unify, we return the unified value as the semantic value;
           if they don't unify, we fail the parse."""
        target = element.target
        if issubclass(type(target), Terminal):
            parser = self.parseTerminal
        elif issubclass(type(target), Nonterminal):
            parser = self.parseNonterminal
        else:
            raise ValueError("Features can only be attached to Terminals and Nonterminals")

        for aparse in parser(target, stream):
            # We're not doing the unification yet
            unified = Feature.unify(element.features, aparse)
            print "Unifying ", element.features, aparse
            if unified:
                yield unified
        
    def parseTerminal(self, element, stream):
        tok = self.currentToken(stream)
        if element.getName() == self.terminalExtractor(tok):
            stream[0] += 1
            if self.debug:
                print "Shifted Terminal", element
            yield self.valueExtractor(tok)
            return

    def currentToken(self, stream):
        return stream[1][stream[0]]
 
    def copyStream(self, stream):
        return [stream[0], stream[1]]


    
