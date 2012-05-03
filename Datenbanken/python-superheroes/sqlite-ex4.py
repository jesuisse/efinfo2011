import sqlite3

db = sqlite3.connect("superheroes.db")

superheld = raw_input("Gib den Namen eines Superhelden ein:")

c = db.cursor()
c.execute("SELECT name, identity FROM superhero WHERE name = ?", [superheld])
rows = c.fetchall()
for row in rows:
    print row[0], "ist in Wahrheit", row[1]
