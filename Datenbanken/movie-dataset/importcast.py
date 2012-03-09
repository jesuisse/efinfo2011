import sqlite3

conn = sqlite3.connect("movies.db")

f = open("cast.txt", "r")
c = conn.cursor()
for line in f:
    actor,title,impersonated = line[:-1].split(",")    
    print actor,title,impersonated
    c.execute("select id from movies where title = ?", (title,))

    for result in c.fetchall():
        movieid = result[0]
        c.execute("insert into moviecast (movieid,actor,impersonated) values (?, ?, ?)", (movieid,actor,impersonated))
     

conn.commit()
