# -*- coding: utf-8 -*-
import sqlite3

db = sqlite3.connect("superheroes.db")

name = raw_input("Superheld:")
identitaet = raw_input("Richtiger Name:")
geschlecht = raw_input("Geschlecht (m/f):")

if geschlecht not in ('m', 'f'):
    print "Du musst m oder f eingeben!"
else:
    c = db.cursor()
    c.execute("""INSERT INTO superhero (name, identity, gender, alignment) 
                  VALUES (?, ?, ?, 'Gut')""", 
              [name, identitaet, geschlecht])
    print "ID für den Eintrag:", c.lastrowid
    db.commit()
