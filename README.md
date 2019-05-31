Unitpy - Because real life has units
==========================

Unitpy is WIP library that allows for creating values with units, which can be used in all variety of calculations. Unitpy prevents calculations that would be invalid with units, like adding values with different units. It also combines units for calculations like multiplication and division and modifies units for exponentiation.

For example:
```{.sourceCode .python}
>>> from unitpy import BaseUnit
>>> X = BaseUnit(5, 'm^3/s')  # 5 cubic meters per second
>>> Y = BaseUnit(10, 'm^3*s^-1')  # 10 cubic meters per second
>>> Z = BaseUnit(12, 'kg/m^3')  # 12 kilograms per cubic meter
>>> X + Y  # Can add values with the same units.
15 m^3/s
>>> Y * Z  # Can multiply values with different units.
120 kg/s
>>> X + Z  # Adding values with different units gives an error
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "D:\Programs\unitpy\unitpy\base_unit.py", line 466, in __add__
    raise UnitMismatchError('Can not add two numbers with different units.')
unitpy.exceptions.UnitMismatchError: Can not add two numbers with different units.
```

Currently only works with base SI units, which are meters, seconds, grams (Used over kg for prefix reasons), amperes, kelvin, mole, candela, and prefixes for them. Units that are made of combinations of these units, like Newton or Pascal, are currently in the works. Classes in unitpy.units are not yet functional.

A unit object's value can be int or float, Decimal type, all int and float types from numpy, or the mpf type from mpmath.

**This is a very early WIP project so breaking changes may occur.**