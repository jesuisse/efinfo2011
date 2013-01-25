from easyparser import *

ft = Feature

def makeLexicon():
    nn = "Krokodil/Pferd/Huhn"
    mn = "Esel/Schwan"
    fn = "Maus/Kuh/Taube"
    mart = "Der/der"
    nart = "Das/das"
    fart = "Die/die/Eine/eine"

    lexicon = {}
    for word in nn.split("/"):
        lexicon[word] = ft(word=word, agr=ft(gen='n'), tag='NN')
    for word in mn.split("/"):
        lexicon[word] = ft(word=word, agr=ft(gen='m'), tag='NN')
    for word in fn.split("/"):
        lexicon[word] = ft(word=word, agr=ft(gen='f'), tag='NN')
    for word in mart.split("/"):
        lexicon[word] = ft(word=word, agr=ft(gen='m'), tag='ART')
    for word in nart.split("/"):
        lexicon[word] = ft(word=word, agr=ft(gen='n'), tag='ART')
    for word in fart.split("/"):
        lexicon[word] = ft(word=word, agr=ft(gen='f'), tag='ART')
    lexicon["_UNKNOWN_"] = ft(word = word, tag="UNKNOWN")
    return lexicon

def _tagger(word, lexicon):
    if word in lexicon:
        return lexicon[word]
    else:
        return lexicon["_UNKNOWN_"]

def makeTagger(lexicon):
    return lambda word: _tagger(word, lexicon)
    
    
s = Nonterminal("s")
art = Nonterminal("Artikel")
nn = Nonterminal("Nomen")

T = Terminal

s >> T("ART") + T("NN")


line = raw_input("Gib was ein: ")
words = line.split(" ")
tagged = []
tagger = makeTagger(makeLexicon())
for word in words:
    tagged.append(tagger(word))
parser = RecursiveDescentParser(lambda t: t.tag, lambda t: t)
p = parser.parse(words)
try:
    semantic = p.next()
    print "Aha, ich verstehe: ", semantic
except StopIteration:
    print "Sorry, das verstehe ich nicht"
    



