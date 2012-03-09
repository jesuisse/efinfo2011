
create table kunden(
    nr integer primary key autoincrement,
    vorname varchar(30) not null,
    nachname varchar(30) not null
);

create table artikel(
    nr integer primary key autoincrement,
    name varchar(30) not null,
    preis real not null
);

create table filialen(
    id integer primary key autoincrement,
    name varchar(30) not null,
    ort varchar(30) not null
);

create table verkauf(
    knr integer references kunden(nr),
    artnr integer references artikel(nr),
    fid integer references filiale(id),
    datum datetime 
);

insert into kunden (vorname, nachname) values ("Alain", "Brunner");
insert into kunden (vorname, nachname) values ("Andreas", "Gruhler");
insert into kunden (vorname, nachname) values ("Balz", "Guenat");
insert into kunden (vorname, nachname) values ("Lukas", "Steiner");
insert into kunden (vorname, nachname) values ("Lukas", "Wenner");
insert into kunden (vorname, nachname) values ("Tibor", "Jonas");

insert into artikel (name, preis) values ("Hammer XSL", 9.95);
insert into artikel (name, preis) values ("Pyjama-Hose", 19.50);
insert into artikel (name, preis) values ("Pyjama-Oberteil Seide", 99.80);
insert into artikel (name, preis) values ("Milch Drink", 1.50);
insert into artikel (name, preis) values ("Kaugummi", 0.90);
insert into artikel (name, preis) values ("Mars", 1.30);
insert into artikel (name, preis) values ("Schraubenzieher", 7.60);
insert into artikel (name, preis) values ("Pouletgeschnetzeltes", 5.70);
insert into artikel (name, preis) values ("Huus-Brot 1kg", 3.20);
insert into artikel (name, preis) values ("Bananen 1kg", 4.50);
insert into artikel (name, preis) values ("Dush-Gel", 8.20);
insert into artikel (name, preis) values ("Gilette Rasierklingen", 18.20);

insert into filialen(name, ort) values ("Bahnhof", "Biel");
insert into filialen(name, ort) values ("Bahnhof", "Bern");
insert into filialen(name, ort) values ("Marktgasse", "Bern");
insert into filialen(name, ort) values ("Hauptstrasse", "Lengnau");

insert into verkauf (knr, artnr, fid) values (1, 1, 1);
insert into verkauf (knr, artnr, fid) values (1, 4, 1);
insert into verkauf (knr, artnr, fid) values (1, 11, 1);
insert into verkauf (knr, artnr, fid) values (2, 4, 4);
insert into verkauf (knr, artnr, fid) values (2, 10, 2);
insert into verkauf (knr, artnr, fid) values (2, 8, 4);
insert into verkauf (knr, artnr, fid) values (2, 6, 1);
insert into verkauf (knr, artnr, fid) values (3, 7, 3);
insert into verkauf (knr, artnr, fid) values (3, 11, 3);
insert into verkauf (knr, artnr, fid) values (4, 2, 1);
insert into verkauf (knr, artnr, fid) values (4, 3, 1);
insert into verkauf (knr, artnr, fid) values (4, 9, 1);
insert into verkauf (knr, artnr, fid) values (4, 12, 1);
insert into verkauf (knr, artnr, fid) values (5, 3, 4);
insert into verkauf (knr, artnr, fid) values (5, 4, 1);
insert into verkauf (knr, artnr, fid) values (5, 9, 1);
insert into verkauf (knr, artnr, fid) values (5, 10, 4);

