import sqlite3

conn = sqlite3.connect("movies.db")

f = open("genres.txt", "r")
c = conn.cursor()
for line in f:
    title,genre = line[:-1].split(",")    
    print title,genre
    c.execute("select id from movies where title = ?", (title,))

    for result in c.fetchall():
        movieid = result[0]
        c.execute("insert into genre (movieid,name) values (?, ?)", (movieid,genre))
     

conn.commit()
