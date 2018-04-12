# TODO: figure out how to pass by value
class Dimension:
    baseUnits = {"length": "m", "mass": "kg", "time": "s", "current": "A", "temperature": "K", "amountOfSubstance": "mol", "luminousIntensity": "cd", "angle": "rad"}
    
    def __init__(self, length=0, mass=0, time=0, current=0, temperature=0, amountOfSubstance=0, luminousIntensity=0, angle=0):
        self.length = length
        self.mass = mass
        self.time = time
        self.current = current
        self.temperature = temperature
        self.amountOfSubstance = amountOfSubstance
        self.luminousIntensity = luminousIntensity
        self.angle = angle
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __add__(self, other):
        return Dimension(**self.__dict__) if self.__dict__ == other.__dict__ else raiser(ValueError("addition with different units"))
    
    def __sub__(self, other):
        return Dimension(**self.__dict__) if self.__dict__ == other.__dict__ else raiser(ValueError("addition with different units"))
    
    def __mul__(self, other):
        unions = {key: (self.__dict__[key] + other.__dict__[key]) for key in self.__dict__.keys() & other.__dict__.keys()}
        return Dimension(**{**self.__dict__, **other.__dict__, **unions})
    
    def __truediv__(self, other):
        unions = {key: (self.__dict__[key] - other.__dict__[key]) for key in self.__dict__.keys() & other.__dict__.keys()}
        return Dimension(**{**self.__dict__, **other.__dict__, **unions})
        
    def __pow__(self, power):
        return Dimension(**{key: self.__dict__[key] * power for key in self.__dict__.keys()})
    
    def __repr__(self):
        return self.__str__()
        #return "length^({}) * mass^({}) * time^({}) * current^({}) * temperature^({}) * amountOfSubstance^({}) * luminousIntensity^({}) * angle^({})".format(self.length, self.mass, self.time, self.current, self.temperature, self.amountOfSubstance, self.luminousIntensity, self.angle)
    
    def __str__(self):
        topKeys = sorted([key for key in self.__dict__.keys() if self.__dict__[key] > 0], key=lambda k: (self.__dict__[k], k))
        bottomKeys = sorted([key for key in self.__dict__.keys() if self.__dict__[key] < 0], key=lambda k: (self.__dict__[k], k))
        top = [Dimension.baseUnits[key] + "^" + str(self.__dict__[key]) if self.__dict__[key] != 1 else Dimension.baseUnits[key] for key in topKeys]
        bottom = [Dimension.baseUnits[key] + "^" + str(-self.__dict__[key]) if self.__dict__[key] != -1 else Dimension.baseUnits[key] for key in bottomKeys]
        if not topKeys and not bottomKeys: # if both are empty (only 0's)
            return ""
        elif topKeys and not bottomKeys: # if only positive powers
            return "*".join(top)
        elif not topKeys and bottomKeys: # if only negative powers
            return "1/" + "*".join(bottom)
        else: # if both positive and negative powers
            return "*".join(top) + "/" + "*".join(bottom)
    
    # TODO: make sqrt overloader

################################################################################
# UTILITIES
################################################################################

def raiser(ex): raise ex
