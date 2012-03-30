create table person (
	id integer primary key autoincrement,
	vorname varchar(30),
	nachname varchar(30),
    email varchar(100) not null
);

create table sindBefreundet (
	id1 integer references person(id),
    id2 integer references person(id)
);

create table status (
    pid integer references person(id),
    inhalt text,
    datum timestamp
);

create table wallpost (
    pid integer references person(id),
    bid integer references person(id),
    inhalt text,
    datum timestamp
);

