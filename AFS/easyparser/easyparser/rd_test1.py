from recursivedescent import Nonterminal, Terminal, Action, RecursiveDescentParser


def boyaction(*semlist):
    print "**** SEMANTIC", semlist, type(semlist), "****"
    return ("BOY", semlist)
    
    

p = Nonterminal("prefix")
    
a = Terminal("a")
b = Terminal("b")
c = Terminal("c")
d = Terminal("d")
e = Terminal("e")
f = Terminal("f")

s = Nonterminal("Satz")
det = Nonterminal("Determinierer")
adj = Nonterminal("Adjektiv")
adjlist = Nonterminal("Adjektiv-Reihung")
art = Nonterminal("Artikel")
numeral = Nonterminal("Numerale")
possesive = Nonterminal("Possesivpronomen")
quantifier = Nonterminal("Quantifizierer")
preposition = Nonterminal("Präposition")
nn = Nonterminal("Nomen")

np = Nonterminal("Nominalphrase")
prepp = Nonterminal("Präpositionalphrase")
vp = Nonterminal("Verbphrase")

s >> np + vp 
np >> det(agr = "?n") + adjlist(agr = "?n") + nn(agr="?n") + prepp
prepp >> preposition + np | None
det >> art | numeral | possesive | quantifier
adjlist >> adj + adjlist | None
art >> Terminal("Der") | Terminal("Das") | Terminal("Die") | Terminal("dem")
numeral >> Terminal("Ein") | Terminal("Zwei") | Terminal("Drei")
possesive >> Terminal("Mein") | Terminal("Dein") | Terminal("Sein")
quantifier >> Terminal("Kein") | Terminal("Einige") | Terminal("Viele") | Terminal("Alle")
preposition >> Terminal("auf") | Terminal("in") | Terminal("unter") | Terminal("neben") | Terminal("hinter") | Terminal("vor") | Terminal("über")
vp >> Terminal("rennt")
nn >> Terminal("Junge") + Action(boyaction) | Terminal("Mädchen") | Terminal("Hügel")
adj >> Terminal("schöne") | Terminal("grosse") | Terminal("braune")

test1 = Nonterminal("Test1")
w = Terminal("Wo")
test1 >> w + Terminal("ist") + np + Terminal("her") | w + Terminal("ist") + np + Terminal("hin")
s >> test1

lr = Nonterminal("left-recursive")
n1 = Nonterminal("n1")
n2 = Nonterminal("n2")
n1 >> d | None
n2 >> e | None
lr >> lr + a | n1(agr = "?x",dekl="?d") + n2 + f(agr="?x", dekl="?d") | n2 + c | None




def test1parsed(*sems):
    return sems[2:]

p = RecursiveDescentParser(s)
p.setParseAction(test1, test1parsed)
g = p.parse(("Wo", "ist", "Der", "Junge", "auf", "dem", "grosse", "Hügel", "hin"))



