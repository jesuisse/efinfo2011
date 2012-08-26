# -*- coding: utf-8 -*-

import sqlite3
import math

# MovieLens-Datenbank
db = sqlite3.connect("ml.db")


def estimateMovieRating(userid, movieid):
    """Schätzt ab, welches Rating die Person mit id userid
       dem Film mit id movieid verleihen würde, und liefert
       das Ergebnis zurück."""
    
    # Liefert im Moment einfach immer 3 zurück. Verbessern!
    return 3.0

def recommendMovies(userid, n):
    """Liefert eine Liste von maximal n movieids zurück, die der Person
       userid gefallen könnten."""

    # Liefert im Moment immer nur "Richard III" und "Seven".
    # Verbessern!
    return [10, 11]

def getTitle(movieid):
    """Liefert den Titel eines Films"""
    global db
    c = db.cursor()
    c.execute("select title from movies where id = ?", [movieid])
    r = c.fetchone()
    return r[0]

# Wie gut mag Benutzer 1 den Film Seven?
print "Person 1 bewertet den Film mit", estimateMovieRating(1, 11)

# Zeigt maximal 5 Filmvorschläge für Benutzer 1 an
print "Filmvorschläge für Person 1:"
for movieid in recommendMovies(1, 5):
    print getTitle(movieid)
    


    
