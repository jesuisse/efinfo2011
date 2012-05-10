
import sqlite3

db = sqlite3.connect("ml.db")
db.text_factory = str
c = db.cursor()

f = open("users.dat", "rt")

while True:
    line = f.readline()
    if line == "":
        break
    if line[-1] == '\n':
        line = line[0:-1]
    data = line.split('|')
    c.execute("INSERT INTO users (id,age,gender,occupation,zip) VALUES (?,?,?,?,?)",
              data)

f.close()

f = open("movies.dat", "rt")

while True:
    line = f.readline()
    if line == "":
        break
    if line[-1] == '\n':
        line = line[0:-1]
    data = line.split('|')
    c.execute("INSERT INTO movies (id,title,released,videoReleased,url,genreUnknown,genreAction,genreAdventure,genreAnimation,genreChildren,genreComedy,genreCrime,genreDocumentary,genreDrama,genreFantasy,genreFilmNoir,genreHorror,genreMusical,genreMystery,genreRomance,genreSciFi,genreThriller,genreWar,genreWestern) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              data)
f.close()
    

f = open("ratings.dat", "rt")

while True:
    line = f.readline()
    if line == "":
        break
    if line[-1] == '\n':
        line = line[0:-1]
    data = line.split()
    c.execute("INSERT INTO ratings (userid,movieid,rating,date) VALUES (?,?,?,?)",
              data)
f.close()

db.commit()


