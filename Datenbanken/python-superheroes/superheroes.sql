CREATE TABLE superhero (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       gender VARCHAR(1),
       name VARCHAR(64),
       identity VARCHAR(64),
       alignment VARCHAR(4)       
);

CREATE TABLE superpower (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       shortname VARCHAR(32),
       description TEXT
);

CREATE TABLE teammembers (
       name NOT NULL,
       heroid INTEGER REFERENCES superhero(id)
);

CREATE TABLE has_power (
       heroid INTEGER REFERENCES superhero(id),
       powerid INTEGER REFERENCES superpower(id)
);

INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Mr Incredible", "m", "Robert Parr", "Gut");
INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Elastigirl", "f", "Helen Parr", "Gut");
INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Dash", "m", "Dashiell Parr", "Gut");
INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Jack-jack", "m", "Jack-jack Parr", "Gut");
INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Invisagirl", "f", "Violet Parr", "Gut");
INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Superman", "m", "Clark Kent", "Gut");
INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Batman", "m", "Bruce Wayne", "Gut");
INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Robin", "m", "Richard John Grayson", "Gut");
INSERT INTO superhero (name, gender, identity, alignment) VALUES ("Spiderman", "m", "Peter Parker", "Gut");

INSERT INTO teammembers (name, heroid) VALUES ("Incredibles", 1);
INSERT INTO teammembers (name, heroid) VALUES ("Incredibles", 2);
INSERT INTO teammembers (name, heroid) VALUES ("Incredibles", 3);
INSERT INTO teammembers (name, heroid) VALUES ("Incredibles", 5);

INSERT INTO teammembers (name, heroid) VALUES ("Batman & Robin", 7);
INSERT INTO teammembers (name, heroid) VALUES ("Batman & Robin", 8);

INSERT INTO superpower (shortname, description) VALUES ("Elastizität", "Verfügt über elastische Gliedmassen, die gestreckt werden können");
INSERT INTO superpower (shortname, description) VALUES ("Superkraft", "Übermenschliche Kräfte");
INSERT INTO superpower (shortname, description) VALUES ("Röntgenblick", "Kann mit den Augen Objekte durchleuchten");
INSERT INTO superpower (shortname, description) VALUES ("Unverwundbarkeit", "Kann durch Impulswaffen, Stösse, Hitze, Kälte usw. nicht verwundet werden");
INSERT INTO superpower (shortname, description) VALUES ("Superschnelligkeit", "Kann sich so schnell bewegen, dass andere die Bewegung von blossem Auge kaum mehr wahrnehmen können");
INSERT INTO superpower (shortname, description) VALUES ("Gestaltwandler", "Kann seine Gestalt verändern");
INSERT INTO superpower (shortname, description) VALUES ("Unsichtbarkeit", "Kann sich unsichtbar machen");
INSERT INTO superpower (shortname, description) VALUES ("Fliegen", "Kann fliegen");

INSERT INTO has_power (heroid, powerid) VALUES(1, 2);
INSERT INTO has_power (heroid, powerid) VALUES(2, 1);
INSERT INTO has_power (heroid, powerid) VALUES(3, 5);
INSERT INTO has_power (heroid, powerid) VALUES(4, 6);
INSERT INTO has_power (heroid, powerid) VALUES(5, 4);
INSERT INTO has_power (heroid, powerid) VALUES(5, 7);
INSERT INTO has_power (heroid, powerid) VALUES(6, 2);
INSERT INTO has_power (heroid, powerid) VALUES(6, 3);
INSERT INTO has_power (heroid, powerid) VALUES(6, 8);
