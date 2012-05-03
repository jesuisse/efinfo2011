import sqlite3

db = sqlite3.connect("superheroes.db")

name = raw_input("Welchen Superhelden entfernen? ")

c = db.cursor()
c.execute("DELETE FROM superhero WHERE name = ?", [name])
db.commit()
