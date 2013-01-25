
class Feature(object):
    """Ein Feature ist ein etwas besseres Dictionary und dient zum Transport
       von grammatischen Eigenschaften."""

    @staticmethod
    def unify(f1, f2, bindings=None):
        """Statische Methode, welche zwei Features f1 und f2 unifiziert und
           das unifizierte Feature-Objekt zurückliefert."""
        return unifyFeatures(f1, f2, bindings)
            
    def __init__(self, **kwargs):
        """Alle kwargs werden zu Attributen des konstruierten Objekts"""                
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getitem__(self, name):        
        return getattr(self, name)

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def __repr__(self):
        akku = []
        for key, value in self.__dict__.items():
            akku.append("%s = %s" % (key, repr(value)))
        return "Feature(" + ", ".join(akku) + ")"

    def __contains__(self, key):
        return hasattr(self, key)
    
    def add(self, **kwargs):
        """Fügt eine beliebige Anzahl features hinzu"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()
    
    def copy(self):
        """Gibt eine exakte shallow-Kopie dieses Features zurück"""
        return Feature(self.__dict__)

def isFeatureVariable(x):
    try:
        return x[0] == "?"    
    except:
        pass
    return False
    

def unifyFeatures(f1, f2, bindings=None):
    """Tries to unify feature structures f1 and f2.
       Currently, this cannot unify variables 
       that should pair with other variables.

       Note: Works both with ordinary python dicts
       and with Feature objects.

       If you are interested in the bindings, you should
       pass in a binding dictionary, which will be
       augmented by unifyFeatures (and maybe invalidated
       if unification fails).

       The return value is the unified feature dictionary,
       or None if f1 and f2 failed to unify. In that case,
       the bindings dictionary you may have passed in will
       contain partial bindings and should be discarded."""
    
    if bindings == None: 
        bindings = {}
    
    k1 = set(f1.keys())
    k2 = set(f2.keys())

    result = {}

    for key in k1.union(k2):
        if key not in f1:
            result[key] = f2[key]
        elif key not in f2:
            result[key] = f1[key]
        elif type(f1[key]) == type(f2[key]) and (type(f1[key]) == dict or issubclass(type(f1[key]), Feature)):
            ft = unifyFeatures(f1[key],  f2[key], bindings)
            if ft == None:
                return None
            else:
                result[key] = ft
        elif f1[key] == f2[key]:
            result[key] = f1[key]            
        elif isFeatureVariable(f1[key]):
            ft = unifyFeatureVariable(f1[key], f2[key], bindings)
            if ft == None:
                return None
            else:
                result[key] = ft                
        elif isFeatureVariable(f2[key]):
            ft = unifyFeatureVariable(f2[key], f1[key], bindings)
            if ft == None:
                return None
            else:
                result[key] = ft                
        else:
            return None
    if issubclass(type(f1), Feature) and issubclass(type(f2), Feature):        
        return Feature(**result)
    else:
        return result
    
def unifyFeatureVariable(variable,  value,  bindings):
    # We don't yet check for the case where value is also a variable!
    if variable in bindings:
        bval = bindings[variable]
        if type(bval) == dict or issubclass(type(bval), Feature):
            return unifyFeatures(bval,  value, bindings)
        elif bval == value:
            return value
        else:
            return None
    else:
        bindings[variable] = value
        return value
        
