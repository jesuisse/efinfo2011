# -*- coding: utf-8 -*-
import sqlite3

db = sqlite3.connect("superheroes.db")
db.text_factory = str

teamname = raw_input("Gib ein Superhelden-Team ein: ")
superkraft = raw_input("Gib eine Superkraft ein: ")

c = db.cursor()
c.execute("""SELECT superhero.name
               FROM superhero, teammembers, has_power, superpower
               WHERE superhero.id = has_power.heroid
                 AND superhero.id = teammembers.heroid
                 AND superpower.id = powerid
                 AND teammembers.name = ?
                 AND shortname = ?""", [teamname, superkraft])

rows = c.fetchall()
for row in rows:
   print row[0], "vom Team", teamname, "hat die Fähigkeit", superkraft
