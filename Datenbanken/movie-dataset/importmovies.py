import sqlite3

conn = sqlite3.connect("movies.db")

f = open("movies.txt", "r")
c = conn.cursor()
for line in f:
    title,year,mppa,director,runtime = line[:-1].split(",")
    year = int(year)
    runtime = int(runtime)
    print title,year,mppa,director,runtime
    c.execute("insert into movies (title,year,mppa,director,runtime) values (?, ?, ?, ?, ?)", (title,year,mppa,director,runtime))
        

conn.commit()
