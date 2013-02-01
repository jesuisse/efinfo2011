# -*- coding: utf-8 -*-

from easyparser.features import Feature
ft = Feature


def features(**kwargs):
    """Erzeugt eine features-Struktur """
    return dict(**kwargs)    
 

# Die Feature-Struktur für das Wort "Jungen"
jungen_feat = features( agr = (
                 features(num="sg", kas="gen"),
                 features(num="sg", kas="acc"),
                 features(num="sg", kas="dat"),
                 features(num="pl", kas="nom"),
                 features(num="pl", kas="acc"),
                 features(num="pl", kas="dat")))

# Die Feature-Struktur für das Wort "Junge"
junge_feat= features(agr = features(num="sg",kas="nom"))
                       
                       
                       
               

