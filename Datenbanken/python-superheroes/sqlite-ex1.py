import sqlite3

f = open("superheroes.sql", "r")
sqlStatements = f.read()
f.close()

db = sqlite3.connect("superheroes.db")
db.executescript(sqlStatements)
db.commit()
db.close()
