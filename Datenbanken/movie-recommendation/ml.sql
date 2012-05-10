
CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	age INTEGER,
	gender VARCHAR(1),
	occupation VARCHAR(50),
	zip INTEGER
);

CREATE TABLE movies (
	id INTEGER PRIMARY KEY,
	title TEXT,
	released TEXT,
	videoReleased TEXT,
	url TEXT,
	genreUnknown INTEGER,
	genreAction INTEGER,
	genreAdventure INTEGER,
	genreAnimation INTEGER,
	genreChildren INTEGER,
	genreComedy INTEGER,
	genreCrime INTEGER,
	genreDocumentary INTEGER,
	genreDrama INTEGER,
	genreFantasy INTEGER,
	genreFilmNoir INTEGER,
	genreHorror INTEGER,
	genreMusical INTEGER,
	genreMystery INTEGER,
	genreRomance INTEGER,
	genreSciFi INTEGER,
	genreThriller INTEGER,
	genreWar INTEGER,
	genreWestern INTEGER
);

CREATE TABLE ratings (
	userid INTEGER REFERENCES users(id),
	movieid INTEGER REFERENCES movies(id),
	rating INTEGER,
	date DATETIME
);

CREATE TABLE alikePersons (
	userid1 INTEGER,
	userid2 INTEGER,
	similarity REAL
);


