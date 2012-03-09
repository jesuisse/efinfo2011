CREATE TABLE movies (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       title VARCHAR(64),
       year INTEGER,
       mppa VARCHAR(5),
       director VARCHAR(64),
       runtime INT
);

CREATE TABLE genre (
       movieid INTEGER,
       name VARCHAR(30),
       FOREIGN KEY(movieid) REFERENCES movies(id)
);

CREATE TABLE cast (       
       movieid INTEGER,
       actor VARCHAR(64),
       impersonated VARCHAR(64),
       FOREIGN KEY(movieid) REFERENCES movies(id)
);
