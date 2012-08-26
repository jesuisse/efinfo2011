# -*- coding: utf-8 -*-
"""
Dieses Programm versucht zu messen, wie ähnlich der Geschmack von zwei
beliebigen Personen in der Datenbank ist. Dazu vergleicht es für jede
Kombination von zwei Personen, wie ähnlich sie Filme bewertet haben.

Das Ergebnis ist eine riesige Tabelle (nur zur Hälfte - diagonal - gefüllt),
welche die Ähnlichkeit misst. 1 = identisch, 0 = komplett verschieden (nicht
mal einen einzigen Film gemeinsam). 
"""

import sqlite3
import math

db = sqlite3.connect("ml.db")
db.text_factory = str

def comparePersons(personA, personB):
    """Nimmt zwei Personen-Ids und liefert einen Ähnlichkeitswert zwischen
       0 und 1 zurück."""

    # Abkürzung
    if personA == personB:
        return 1.0

    nCommonMovies = 0
    similarity = 0.0

    c= db.cursor()    
    c.execute("""SELECT a.movieid, a.rating, b.rating FROM ratings AS a, ratings AS b
                 WHERE a.movieid = b.movieid AND a.userid = ? and b.userid = ?""",
              (personA, personB))
    commonMovies = c.fetchall()
    nCommonMovies = len(commonMovies)
    if nCommonMovies > 0:
        for dummy, ratingA, ratingB in commonMovies:
            similarity += (ratingA - ratingB) ** 2
        similarity = 1.0 - math.tanh(math.sqrt(similarity / nCommonMovies))
        
    return similarity


def buildPersonSimilarityTable():
    """Erzeugt eine Tabelle, in der Ähnlichkeitswerte für alle Personen
       stehen..."""
    
    c = db.cursor()    
    c.execute("SELECT id FROM users ORDER BY id")
    userids = c.fetchall()
    nUsers = len(userids)
    count = 0

    c.execute("SELECT max(userid1) FROM alikePersons")
    r = c.fetchone()
    if r[0] == None:
        startA = 0
        startB = 0
    else:        
        startA = r[0]-1
        c.execute("SELECT max(userid2) FROM alikePersons WHERE userid1 = ?", [startA+1])
        r = c.fetchone()
        startB = r[0]
        if startB > startA:
            startA+= 1
            startB = 0

    count = 0
   
    print "Starting at", startA, startB, "for a total of", nUsers, "persons."
    # complete last unfinished row
    for x in xrange(startB, startA+1):
            sim=comparePersons(userids[startA][0], userids[x][0])
            c.execute("INSERT INTO alikePersons (userid1, userid2, similarity) VALUES (?,?,?)",
                        (userids[startA][0], userids[x][0], sim))
            count += 1                
            if count % 100 == 0:
                print count
                db.commit()
    
    # compute all following rows
    for y in xrange(startA+1, nUsers):
        for x in xrange(0, y+1):
            sim=comparePersons(userids[y][0], userids[x][0])
            c.execute("INSERT INTO alikePersons (userid1, userid2, similarity) VALUES (?,?,?)",
                        (userids[y][0], userids[x][0], sim))
            count += 1                
            if count % 100 == 0:
                print count
                db.commit()
                          
        
buildPersonSimilarityTable()    








    
        


