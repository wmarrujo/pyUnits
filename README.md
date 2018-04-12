# pyUnits

A python library for handling units and measurements.

## Usage

import the Measure python file:
```python
from Measure import *
```

The primary object you will interact with is the `Measure` object.
This object acts like a normal floating point number except it has a unit attached.

To initialize a measure, you define it like so:
```python
x = Measure(5, "N")
y = Measure(4185.5, "J/kg*K")
# NOTE: implicit parentheses right of '/' eg.: (J)/(kg*K)
```

This prints with a pretty-printed string:
```
>>> x
5.0 [m*kg/s^2.0]
>>> y
4185.5 [m^2.0/s^2.0*K]
```

To get a value in a certain unit, call it as a subscripted argument:
```
>>> x["lbf"]
1.1240451236674445
>>> y["J/kg*K"]
4185.5
```

## Structure

The `Measure` object acts as a floating point number, implementing all the math operators. The `Dimension` object represents the dimension of a measure, having values for each base SI dimensions (including angles as a dimension).
