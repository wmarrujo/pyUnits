from Unit import *
import re
from functools import reduce

class Measure:
    def __init__(self, value, unit):
        """
        value :: Number
        dimension :: Dimension
        """
        (m, d) = readUnit(unit)
        self.value = m*value
        self.dimension = d
    
    def __eq__(self, other):
        return self.value == other.value and self.dimension == other.dimension
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        if self.dimension != other.dimension:
            raise ValueError("cannot compare measures with different dimensions")
        return self.value < other.value
    
    def __le__(self, other):
        if self.dimension != other.dimension:
            raise ValueError("cannot compare measures with different dimensions")
        return self.value <= other.value
    
    def __ge__(self, other):
        if self.dimension != other.dimension:
            raise ValueError("cannot compare measures with different dimensions")
        return self.value >= other.value
    
    def __gt__(self, other):
        if self.dimension != other.dimension:
            raise ValueError("cannot compare measures with different dimensions")
        return self.value > other.value
    
    def __pos__(self):
        return Measure(+self.value, self.dimension)
    
    def __neg__(self):
        return Measure(-self.value, self.dimension)
    
    def __abs__(self):
        return Measure(abs(self.value), self.dimension)
    
    def __add__(self, other):
        return Measure(self.value + other.value, self.dimension + other.dimension)
    
    def __iadd__(self, other):
        self.value += other.value
        self.dimension += other.dimension
    
    def __sub__(self, other):
        return Measure(self.value - other.value, self.dimension - other.dimension)
    
    def __isub__(self, other):
        self.value -= other.value
        self.dimension -= other.dimension
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Measure(self.value * other.value, self.dimension * other.dimension)
        else:
            return Measure(self.value * other, self.dimension)
    
    def __rmul__(self, other):
        if isinstance(other, self.__class__):
            return Measure(other.value * self.value, other.dimension * self.dimension)
        else:
            return Measure(other * self.value, self.dimension)
    
    def __imul__(self, other):
        if isinstance(other, self.__class__):
            self.value *= other.value
            self.dimension *= other.dimension
        else:
            self.value *= other
    
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Measure(self.value / other.value, self.dimension / other.dimension)
        else:
            return Measure(self.value / other, self.dimension)
    
    def __rtruediv__(self, other):
        if isinstance(other, self.__class__):
            return Measure(other.value / self.value, other.dimension / self.dimension)
        else:
            return Measure(other / self.value, 1/self.dimension)
    
    def __itruediv__(self, other):
        if isinstance(other, self.__class__):
            self.value /= other.value
            self.dimension /= other.dimension
        else:
            self.value /= other
    
    def __pow__(self, power):
        return Measure(self.value ** power, self.dimension ** power)
    
    def __ipow__(self, power):
        self.value **= power
        self.dimension **= power
    
    def __int__(self):
        return self.__trunc__().value
    
    def __float__(self, digits=None):
        return Measure(float(self.value, digits), self.dimension)
    
    def __round__(self):
        return Measure(round(self.value), self.dimension)
    
    def __trunc__(self):
        return Measure(trunc(self.value), self.dimension)
    
    def __ceil__(self):
        return Measure(ceil(self.value), self.dimension)
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return str(self.value) + " [" + str(self.dimension) + "]"
    
    def __getitem__(self, key):
        (m, d) = readUnit(key)
        return self.value/m # get value from base units

def readUnit(unitString):
    """
    readUnit :: String -> (Number, Dimension)
    takes the unit as a string
    returns the multiplier to baseUnits and the dimension
    """
    # TODO: make it work with powers of rational numbers. ex: "m^(1/2)"
    # split by "/"
    sides = unitString.split("/")
    top = sides[0] if len(sides) >= 1 else []
    if top == ["1"]:
        top = [] # then it's a 1/unit
    bottom = sides[1] if len(sides) == 2 else []
    # split by "*"
    topTerms = top.split("*") if len(sides) >= 1 and not unitString.startswith("1") else []
    bottomTerms = bottom.split("*") if len(sides) == 2 else []
    # split by "^" or read "²"
    topUnits = [readDimensionTerm(term) for term in topTerms]
    bottomUnits = [readDimensionTerm(term) for term in bottomTerms]
    units = topUnits + [(u, -p) for (u, p) in bottomUnits]
    # match with multipliers
    unitStats = [(getUnitMultiplierAndDimension(u), p) for (u, p) in units] # [((multiplier, Dimension), power)]
    unitStats = [(m**p, d**p) for ((m, d), p) in unitStats] # apply power to multiplier and dimension
    # multiply together all the multipliers and dimensions
    x = reduce(lambda a, b: (a[0] * b[0], a[1] * b[1]), unitStats)
    return x

def readDimensionTerm(term):
    """
    readDimensionTerm :: String -> (String, Number)
    takes the term string in the form "kg" or "kg^2" or "kg²"
    returns the unit string ("kg") and the power (2)
    """
    # split term string into the unit and the power
    unit = re.match(r"([a-zA-Zα-ωΑ-Ω]|°|Å)+", term).group(0)
    rest = term.lstrip(unit)
    # disect the power to get the number
    if rest == "": # no power written
        power = 1
    elif rest.startswith("^"): # if it contains numbers
        power = float(rest.lstrip("^"))
    else: # if it contains superscripted numbers
        power = float("".join([unitPowerReplacements[char] for char in rest]))
    # return the unit and the power
    return (unit, power)

def getUnitMultiplierAndDimension(unit):
    """
    getUnitMultiplierAndDimension :: String -> (Number, Dimension)
    takes the unit string
    returns the multiplier to base units and the dimension of that unit
    """
    # get the associated multiplier and dimension or unit
    (m, d) = unitInformation[unit]
    # test if it returned a reference unit
    if isinstance(d, str): # if it returned a string
        (nm, nd) = readUnit(d)
        return (m*nm, nd)
    else:
        return (m, d)

# READ: https://docs.python.org/3/reference/datamodel.html

# TODO: also make Measures work with sqrt

unitPowerReplacements = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9"}

# unitInformation :: {unit: (multiplier, dimension|unitstring)}
# !!!: be sure this does not have any unit reference loops
unitInformation = {
    # Base SI
    
    "m": (1, Dimension(length=1)),
    "kg": (1, Dimension(mass=1)),
    "s": (1, Dimension(time=1)),
    "A": (1, Dimension(current=1)),
    "K": (1, Dimension(temperature=1)),
    "mol": (1, Dimension(amountOfSubstance=1)),
    "cd": (1, Dimension(luminousIntensity=1)),
    "rad": (1, Dimension(angle=1)),
    
    # Length
    "Ym": (1e24, "m"),
    "Zm": (1e21, "m"),
    "Em": (1e18, "m"),
    "Pm": (1e15, "m"),
    "Tm": (1e12, "m"),
    "Gm": (1e9, "m"),
    "Mm": (1e6, "m"),
    "km": (1e3, "m"),
    "hm": (1e2, "m"),
    "dam": (1e1, "m"),
    "dm": (1e-1, "m"),
    "cm": (1e-2, "m"),
    "mm": (1e-3, "m"),
    "μm": (1e-6, "m"),
    "nm": (1e-9, "m"),
    "pm": (1e-12, "m"),
    "fm": (1e-15, "m"),
    "am": (1e-18, "m"),
    "zm": (1e-21, "m"),
    "ym": (1e-24, "m"),
    
    "Å": (1e-10, "m"),
    "in": (0.0254, "m"),
    "ft": (12, "in"),
    "yd": (3, "ft"),
    "mi": (1760, "yd"),
    "nmi": (1852, "m"),
    "ly": (9.461e15, "m"),
    "AU": (149597870700, "m"),
    "pc": (30856775814671900, "m"),
    "ftm": (72, "in"),
    
    # Mass
    "Yg": (1e21, "kg"),
    "Zg": (1e18, "kg"),
    "Eg": (1e15, "kg"),
    "Pg": (1e12, "kg"),
    "Tg": (1e9, "kg"),
    "Gg": (1e6, "kg"),
    "Mg": (1e3, "kg"),
    "hg": (1e-1, "kg"),
    "dag": (1e-2, "kg"),
    "g": (1e-3, "kg"),
    "dg": (1e-4, "kg"),
    "cg": (1e-5, "kg"),
    "mg": (1e-6, "kg"),
    "μg": (1e-9, "kg"),
    "ng": (1e-12, "kg"),
    "pg": (1e-15, "kg"),
    "fg": (1e-18, "kg"),
    "ag": (1e-21, "kg"),
    "zg": (1e-24, "kg"),
    "yg": (1e-27, "kg"),
    
    "oz": (35.274, "kg"),
    "lbm": (2.20462, "kg"),
    "st": (0.157473, "kg"),
    # TODO: add slugs
    
    # Time
    "Ys": (1e24, "s"),
    "Zs": (1e21, "s"),
    "Es": (1e18, "s"),
    "Ps": (1e15, "s"),
    "Ts": (1e12, "s"),
    "Gs": (1e9, "s"),
    "Ms": (1e6, "s"),
    "ks": (1e3, "s"),
    "hs": (1e2, "s"),
    "das": (1e1, "s"),
    "ds": (1e-1, "s"),
    "cs": (1e-2, "s"),
    "ms": (1e-3, "s"),
    "μs": (1e-6, "s"),
    "ns": (1e-9, "s"),
    "ps": (1e-12, "s"),
    "fs": (1e-15, "s"),
    "as": (1e-18, "s"),
    "zs": (1e-21, "s"),
    "ys": (1e-24, "s"),
    
    "min": (60, "s"),
    "hr": (60, "min"),
    "day": (24, "hr"),
    "days": (24, "hr"),
    "week": (7, "day"),
    "weeks": (7, "day"),
    
    # Temperature
    "YK": (1e24, "K"),
    "ZK": (1e21, "K"),
    "EK": (1e18, "K"),
    "PK": (1e15, "K"),
    "TK": (1e12, "K"),
    "GK": (1e9, "K"),
    "MK": (1e6, "K"),
    "kK": (1e3, "K"),
    "hK": (1e2, "K"),
    "daK": (1e1, "K"),
    "dK": (1e-1, "K"),
    "cK": (1e-2, "K"),
    "mK": (1e-3, "K"),
    "μK": (1e-6, "K"),
    "nK": (1e-9, "K"),
    "pK": (1e-12, "K"),
    "fK": (1e-15, "K"),
    "aK": (1e-18, "K"),
    "zK": (1e-21, "K"),
    "yK": (1e-24, "K"),
    
    "degR": (5/9, "K"),
    "°R": (5/9, "K"),
    
    # Current
    "YA": (1e24, "A"),
    "ZA": (1e21, "A"),
    "EA": (1e18, "A"),
    "PA": (1e15, "A"),
    "TA": (1e12, "A"),
    "GA": (1e9, "A"),
    "MA": (1e6, "A"),
    "kA": (1e3, "A"),
    "hA": (1e2, "A"),
    "daA": (1e1, "A"),
    "dA": (1e-1, "A"),
    "cA": (1e-2, "A"),
    "mA": (1e-3, "A"),
    "μA": (1e-6, "A"),
    "nA": (1e-9, "A"),
    "pA": (1e-12, "A"),
    "fA": (1e-15, "A"),
    "aA": (1e-18, "A"),
    "zA": (1e-21, "A"),
    "yA": (1e-24, "A"),
    
    # Amount of Substance
    "Ymol": (1e24, "mol"),
    "Zmol": (1e21, "mol"),
    "Emol": (1e18, "mol"),
    "Pmol": (1e15, "mol"),
    "Tmol": (1e12, "mol"),
    "Gmol": (1e9, "mol"),
    "Mmol": (1e6, "mol"),
    "kmol": (1e3, "mol"),
    "hmol": (1e2, "mol"),
    "damol": (1e1, "mol"),
    "dmol": (1e-1, "mol"),
    "cmol": (1e-2, "mol"),
    "mmol": (1e-3, "mol"),
    "μmol": (1e-6, "mol"),
    "nmol": (1e-9, "mol"),
    "pmol": (1e-12, "mol"),
    "fmol": (1e-15, "mol"),
    "amol": (1e-18, "mol"),
    "zmol": (1e-21, "mol"),
    "ymol": (1e-24, "mol"),
    
    # Luminous Intensity
    "Ycd": (1e24, "cd"),
    "Zcd": (1e21, "cd"),
    "Ecd": (1e18, "cd"),
    "Pcd": (1e15, "cd"),
    "Tcd": (1e12, "cd"),
    "Gcd": (1e9, "cd"),
    "Mcd": (1e6, "cd"),
    "kcd": (1e3, "cd"),
    "hcd": (1e2, "cd"),
    "dacd": (1e1, "cd"),
    "dcd": (1e-1, "cd"),
    "ccd": (1e-2, "cd"),
    "mcd": (1e-3, "cd"),
    "μcd": (1e-6, "cd"),
    "ncd": (1e-9, "cd"),
    "pcd": (1e-12, "cd"),
    "fcd": (1e-15, "cd"),
    "acd": (1e-18, "cd"),
    "zcd": (1e-21, "cd"),
    "ycd": (1e-24, "cd"),
    
    # Area
    "are": (100, "m^2"),
    "ares": (100, "m^2"),
    "hectare": (100, "are"),
    "hectares": (100, "are"),
    "acre": (4840, "yd^2"),
    "acres": (4840, "yd^2"),
    
    # Volume
    "L": (1000, "m^3"),
    # TODO: do prefixes for L
    "cc": (1, "cm^3"),
    "barrel": (0.158987294928, "m^3"),
    "barrels": (0.158987294928, "m^3"),
    "gal": (3.78541, "L"),
    "qt": (0.25, "gal")
    
    # Frequency
    "Hz": (1, "1/s"),
    
    "YHz": (1e24, "Hz"),
    "ZHz": (1e21, "Hz"),
    "EHz": (1e18, "Hz"),
    "PHz": (1e15, "Hz"),
    "THz": (1e12, "Hz"),
    "GHz": (1e9, "Hz"),
    "MHz": (1e6, "Hz"),
    "kHz": (1e3, "Hz"),
    "hHz": (1e2, "Hz"),
    "daHz": (1e1, "Hz"),
    "dHz": (1e-1, "Hz"),
    "cHz": (1e-2, "Hz"),
    "mHz": (1e-3, "Hz"),
    "μHz": (1e-6, "Hz"),
    "nHz": (1e-9, "Hz"),
    "pHz": (1e-12, "Hz"),
    "fHz": (1e-15, "Hz"),
    "aHz": (1e-18, "Hz"),
    "zHz": (1e-21, "Hz"),
    "yHz": (1e-24, "Hz"),
    
    # Force
    "N": (1, "kg*m/s^2"),
    
    "YN": (1e24, "N"),
    "ZN": (1e21, "N"),
    "EN": (1e18, "N"),
    "PN": (1e15, "N"),
    "TN": (1e12, "N"),
    "GN": (1e9, "N"),
    "MN": (1e6, "N"),
    "kN": (1e3, "N"),
    "hN": (1e2, "N"),
    "daN": (1e1, "N"),
    "dN": (1e-1, "N"),
    "cN": (1e-2, "N"),
    "mN": (1e-3, "N"),
    "μN": (1e-6, "N"),
    "nN": (1e-9, "N"),
    "pN": (1e-12, "N"),
    "fN": (1e-15, "N"),
    "aN": (1e-18, "N"),
    "zN": (1e-21, "N"),
    "yN": (1e-24, "N"),
    
    "lbm": (4.44822, "N"),
    
    # Pressure
    "Pa": (1, "N/m^2"),
    
    "YPa": (1e24, "Pa"),
    "ZPa": (1e21, "Pa"),
    "EPa": (1e18, "Pa"),
    "PPa": (1e15, "Pa"),
    "TPa": (1e12, "Pa"),
    "GPa": (1e9, "Pa"),
    "MPa": (1e6, "Pa"),
    "kPa": (1e3, "Pa"),
    "hPa": (1e2, "Pa"),
    "daPa": (1e1, "Pa"),
    "dPa": (1e-1, "Pa"),
    "cPa": (1e-2, "Pa"),
    "mPa": (1e-3, "Pa"),
    "μPa": (1e-6, "Pa"),
    "nPa": (1e-9, "Pa"),
    "pPa": (1e-12, "Pa"),
    "fPa": (1e-15, "Pa"),
    "aPa": (1e-18, "Pa"),
    "zPa": (1e-21, "Pa"),
    "yPa": (1e-24, "Pa"),
    
    "bar": (1e5, "Pa"),
    "atm": (101325, "Pa"),
    
    # Energy
    "J": (1, "kg*N"),
    
    "YJ": (1e24, "J"),
    "ZJ": (1e21, "J"),
    "EJ": (1e18, "J"),
    "PJ": (1e15, "J"),
    "TJ": (1e12, "J"),
    "GJ": (1e9, "J"),
    "MJ": (1e6, "J"),
    "kJ": (1e3, "J"),
    "hJ": (1e2, "J"),
    "daJ": (1e1, "J"),
    "dJ": (1e-1, "J"),
    "cJ": (1e-2, "J"),
    "mJ": (1e-3, "J"),
    "μJ": (1e-6, "J"),
    "nJ": (1e-9, "J"),
    "pJ": (1e-12, "J"),
    "fJ": (1e-15, "J"),
    "aJ": (1e-18, "J"),
    "zJ": (1e-21, "J"),
    "yJ": (1e-24, "J"),
    
    # Power
    "W": (1, "J/s"),
    
    "YW": (1e24, "W"),
    "ZW": (1e21, "W"),
    "EW": (1e18, "W"),
    "PW": (1e15, "W"),
    "TW": (1e12, "W"),
    "GW": (1e9, "W"),
    "MW": (1e6, "W"),
    "kW": (1e3, "W"),
    "hW": (1e2, "W"),
    "daW": (1e1, "W"),
    "dW": (1e-1, "W"),
    "cW": (1e-2, "W"),
    "mW": (1e-3, "W"),
    "μW": (1e-6, "W"),
    "nW": (1e-9, "W"),
    "pW": (1e-12, "W"),
    "fW": (1e-15, "W"),
    "aW": (1e-18, "W"),
    "zW": (1e-21, "W"),
    "yW": (1e-24, "W"),
    
    }
