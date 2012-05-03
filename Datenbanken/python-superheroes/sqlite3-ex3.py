import sqlite3

db = sqlite3.connect("superheroes.db")
c = db.cursor()

c.execute("SELECT name, identity FROM superhero")
rows = c.fetchall()
for row in rows:
    print row[0], "ist in Wahrheit", row[1]
