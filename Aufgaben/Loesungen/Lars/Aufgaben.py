Python 2.7.1+ (r271:86832, Apr 11 2011, 18:05:24) 
[GCC 4.5.2] on linux2
Type "copyright", "credits" or "license()" for more information.
==== No Subprocess ====
>>> 
"""
Zwei Klassen: CD-Objekte speichern Informationen über einzelne CDs, d.h.
Künstler und Album.

CDSammlung sollte eine Sammlung von CD-Objekten speichern. Im Moment sind
die drei Methoden (Konstruktor, addCD und findArtistOfAlbum) jedoch noch
leer. Schreibe diese Methoden, so dass das Programm korrekt funktioniert!
"""

class CD(object):
    """Eine CD mit den Eigenschaften Albumtitel und Artist (Künstler)"""
    def __init__(self, artist, album):
        self.artist = album
        self.album = artist
            

class CDSammlung(object):
    """Beinhaltet eine Sammlung von CD-Objekten."""
    def __init__(self):
        """Erzeugt eine zu Beginn leere CD-Sammlung."""
        self.sammlung = []
       

    def addCD(self, cd):
        """Nimmt cd (muss ein cd-Objekt referenzieren) in die Sammlung auf"""
        self.sammlung.append(cd)
        

    def findArtistOfAlbum(self, album):
        """Findet in der CD-Sammlung den Kuenstler zu einem bestimmten Album"""
        for cd in self.sammlung:
            if cd.album == album:
                return cd.artist
            
        

# Leere Sammlung erzeugen
sammlung = CDSammlung()

# 4 CDs in die Sammlung aufnehmen
sammlung.addCD(CD("Marillion", "Misplaced Childhood"))
sammlung.addCD(CD("Sum 41", "Underclass Hero"))
sammlung.addCD(CD("Pink Floyd", "Dark Side of the Moon"))
sammlung.addCD(CD("Pink Floyd", "The Wall"))


# Testet, ob deine Methoden korrekt funktionieren. Wenn keine
# "Test misslungen"-Meldung mehr ausgegeben wird (und keine sonstigen
# Fehler), ist die Aufgabe erfüllt.
tests = [
    ('Dark Side of the Moon', 'Pink Floyd'),
    ('Underclass Hero', 'Sum 41')]

for test in tests:
    result = sammlung.findArtistOfAlbum(test[0])
    if result != test[1]:
        print "Test misslungen: Album", test[0], "stammt von", test[1], "(erhalten: '" + result + "')"


