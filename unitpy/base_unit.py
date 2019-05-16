import six
from math import trunc, ceil, floor
from decimal import Decimal
from unitpy.exceptions import *


'''
SI base units (from https://en.wikipedia.org/wiki/International_System_of_Units)

      Dimension                    |        Unit
Symbol       Description           | Name       Symbol
T            time                  | second	    s
L            length                | metre	    m
M            mass	               | kilogram	kg
I            electric current	   | ampere	    A
Θ (K used)   thermodynamic temp.   | kelvin	    K
N            amount of substance   | mole	    mol
J            luminous intensity	   | candela    cd
'''

# TODO
"""
Currently can follow base units through calculation and throw errors for breaking unit rules.
Need to be able to work with non-base units and convert.  
"""

implicit_dimensionless = False  # Disables check in multiplication and division, which checks whether a value has been
                                # declared as dimensionless.

NUMERICS = six.integer_types + (float, Decimal)

try:  # check if Numpy is installed and add its types to NUMERICS.
    import numpy as np
    numpy_types = (np.int8, np.uint8, np.int16, np.uint16, np.int32, np.uint32, np.int64, np.uint64, np.float16,
                   np.float32, np.float64, np.short, np.ushort, np.intc, np.uintc, np.int_, np.uint, np.longlong,
                   np.ulonglong, np.single, np.double, np.long, np.longdouble, np.csingle, np.cdouble, np.clongdouble,
                   np.intp, np.uintp,)
    NUMERICS += numpy_types
except ImportError:
    pass

try:  # check if mpmath is installed and add mpf, a high precision float type, to NUMERICS.
    from mpmath import mpf
    NUMERICS += (mpf,)
except ImportError:
    pass


class BaseUnit:
    STANDARD_UNIT = None
    ALIAS = {}
    UNITS = {}
    SI_PREFIXES = {
        'y': 'yocto',
        'z': 'zepto',
        'a': 'atto',
        'f': 'femto',
        'p': 'pico',
        'n': 'nano',
        'u': 'micro',
        'm': 'milli',
        'c': 'centi',
        'd': 'deci',
        'da': 'deca',
        'h': 'hecto',
        'k': 'kilo',
        'M': 'mega',
        'G': 'giga',
        'T': 'tera',
        'P': 'peta',
        'E': 'exa',
        'Z': 'zeta',
        'Y': 'yotta',
        'NA': 'NA',
    }
    SI_MAGNITUDES = {
        'yocto': 1e-24,
        'zepto': 1e-21,
        'atto': 1e-18,
        'femto': 1e-15,
        'pico': 1e-12,
        'nano': 1e-9,
        'micro': 1e-6,
        'milli': 1e-3,
        'centi': 1e-2,
        'deci': 1e-1,
        'deca': 1e1,
        'hecto': 1e2,
        'kilo': 1e3,
        'mega': 1e6,
        'giga': 1e9,
        'tera': 1e12,
        'peta': 1e15,
        'exa': 1e18,
        'zeta': 1e21,
        'yotta': 1e24,
        'NA': 1,
    }
    SI_UNITS = {'g': 'M',  # SI units with prefixes. Have to use grams over kg for consitency.
                'A': 'I',
                'cd': 'J',
                'm': 'L'}

    def __init__(self, value, unit_input, frac_format=True):
        """

        :param value: Numerical value for measurement.
        :param unit_input: Input for units. Can be either string, in either fractional or exponential format,
        or a list of unit defs.
        :param frac_format: Determines whether the result is printed in the fractional format or exponential format.
        """
        self.value = value
        self.SI_dict = {'T': 's',
                        'L': 'm',
                        'M': 'kg',
                        'I': 'a',
                        'K': 'k',
                        'N': 'mol',
                        'J': 'cd'}
        self.unit_to_base = {
            '1': 'inverse',  # Used for inverse units like 1/m.
            "g": "M",
            "tonne": "M",
            "oz": "M",
            "troy_oz": "M",
            "short_ton": "M",
            "long_ton": "M",
            "gr": "M",
            "stone": "M",
            "carat": "M",
            "solar_mass": "M",
            "earth_mass": "M",
            "s": "T",
            "min": "T",
            "hr": "T",
            "day": "T",
            "c": "K",
            "k": "K",
            "f": "K",
            "r": "K",
            "mol": "N",
            "cd": "J",
            "cp": "J",
            "hk": "J",
            "chain": 'L',
            "chain_benoit": 'L',
            "chain_sears": 'L',
            "british_chain_benoit": 'L',
            "british_chain_sears": 'L',
            "british_chain_sears_truncated": 'L',
            "british_ft": 'L',
            "british_yd": 'L',
            "clarke_ft": 'L',
            "clarke_link": 'L',
            "fathom": 'L',
            "ft": 'L',
            "german_m": 'L',
            "gold_coast_ft": 'L',
            "indian_yd": 'L',
            "inch": 'L',
            "link": 'L',
            "link_benoit": 'L',
            "link_sears": 'L',
            "m": 'L',
            "mi": 'L',
            "nm_uk": 'L',
            "rod": 'L',
            "sears_yd": 'L',
            "survey_ft": 'L',
            "yd": 'L',
            "A": 'I',
        }
        self.is_dimensionless = False
        self.frac_format = frac_format

        if type(unit_input) == list:  # Differentiates from unit entered as str and unit list.
            for unit_def in unit_input:  # Check format of unit def dicts in unit_input.
                keys = list(unit_def.keys())
                if not (type(unit_input[0]) == dict and keys == ['dim', 'order', 'prefix']):
                    raise UnitError("BaseUnit received improperly formatted unit list. {} "
                                    "Should be in format {{'dim': '?', 'order': ?, 'prefix': '?'}}, where dim is the "
                                    "dimension type as a string, order is the exponent of the unit, and prefix is the "
                                    "SI prefix as a string.".format(unit_input))
            self.unit_defs = unit_input  # Accepts unit dict input.
        elif type(unit_input) == str:
            self.unit_defs = self.parse_unit_string(unit_input)
        else:
            raise UnitError('Unit input should be either a string or list of unit definitions.')

    def set_format(self, frac_format):
        """
        Set format as either fractional or exponential.
        :param frac_format: If True format == fractional, else format == exponential.
        :return: None
        """
        self.frac_format = frac_format

    def parse_unit_string(self, unit_str):
        """
        This function builds unit dicts (Dict[str, str, str, int, str, str]{'dim': '?', 'order': ?, 'prefix': '?'}) from
        string. Should work in strings using fraction format (i.e. m*kg^2/s^2) or exponent
        format (i.e. m*kg^2*s^-2).

        :param unit_str: Units given in either fraction or exponent format.
        :return: List of unit defs.
        """

        strip_table = str.maketrans({r'(': r'', r')': r'', r'[': r'', r']': r'', r'{': r'', r'}': r''})
        unit_str = unit_str.translate(strip_table)
        initial_split = unit_str.split('/')  # Splits numerator and denominator

        inferred_fractional = len(initial_split) == 2
        if len(initial_split) > 2:
            raise UnitError("More than one divisor (i.e. '/') is not allowed.")

        if inferred_fractional:
            nume, denom = initial_split
        else:
            nume = initial_split[0]

        split_num = nume.split('*')
        unit_list = []
        for item in split_num:
            if '1' in item and len(item) > 1:
                raise UnitError('1 must be alone when using an inverse unit.')
            order_splt = item.split('^')
            if not order_splt[0].isalpha() and order_splt[0] != '1':
                raise UnitError('Numbers are not allowed in units except for in the case of inverse units, 1/m, and'
                                ' exponents, m^2')
            if len(order_splt) == 2:
                unit, order = order_splt
                try:
                    order = int(order)
                except ValueError:
                    raise UnitError('Exponent should be given as a float in a string (i.e. "m^2" not "m^2.56" or "m^k"')
            elif '^' in item:
                raise UnitError('Unit has "^" but no exponent.')
            else:
                unit = order_splt[0]
                order = 1

            trimmed_unit, prefix = self.sep_unit_prefix(unit)
            dimension = self.unit_to_base[trimmed_unit]
            unit_dict = {'dim': dimension, 'order': order, 'prefix': prefix}
            unit_list.append(unit_dict)

        if inferred_fractional:
            split_denom = denom.split('*')
            for item in split_denom:
                order_splt = item.split('^')
                if not order_splt[0].isalpha():
                    raise UnitError("May not have numbers in the denominator except in exponents.")
                if len(order_splt) == 2:
                    unit, order = order_splt
                    order = -int(order)
                elif '^' in item:
                    raise UnitError('Unit has "^" but no exponent.')
                else:
                    unit = order_splt[0]
                    order = -1
                trimmed_unit, prefix = self.sep_unit_prefix(unit)
                dimension = self.unit_to_base[trimmed_unit]
                unit_dict = {'dim': dimension, 'order': order, 'prefix': prefix}
                unit_list.append(unit_dict)

        return unit_list

    def build_unit_string(self):
        """
        Builds string of units in showing exponents as positive and negative exponents in denominator (+1 excluded).
        Would make m/s instead of m*s^-1.

        :return: Unit string with negative exponents as denominator.
        """
        num_list = []
        denom_list = []
        for unit_def in self.unit_defs:
            if unit_def['dim'] == 'inverse':  # If inverse unit (i.e. 1/m) numerator should be only one
                num_list.append('1')
            else:
                unit_symbol = self.SI_dict[unit_def['dim']]
                unit_order = unit_def['order']

                if unit_order == 1 or unit_order == -1:
                    unit = "{}".format(unit_symbol)
                else:
                    unit = "{}^{}".format(unit_symbol, abs(unit_order))

                if unit_order > 0:
                    if '1' in num_list:  # Removes inverse 1 if more than one value in numerator
                        num_list.remove('1')
                    num_list.append(unit)
                elif unit_order < 0:
                    denom_list.append(unit)

        numerator = "*".join(num_list)
        denominator = "*".join(denom_list)
        
        return "{}/{}".format(numerator, denominator)

    def build_exp_unit_string(self):
        """
        Builds string of units in showing all exponents, except for +1. Would make m*s^-1 instead of  m/s.

        :return: Unit string with negative exponents included.
        """
        unit_list = []
        for unit_def in self.unit_defs:
            unit_symbol = self.SI_dict[unit_def['dim']]
            unit_order = unit_def['order']
            if unit_order == 1:
                unit = "{}".format(unit_symbol)
            else:
                unit = "{}^{}".format(unit_symbol, unit_order)

            if unit_order != 0:
                unit_list.append(unit)

        return "*".join(unit_list)

    def sep_unit_prefix(self, unit_w_prefix):
        trimmed_unit = unit_w_prefix[1:]
        if trimmed_unit in self.SI_UNITS:
            prefix = unit_w_prefix[0]
            return trimmed_unit, prefix
        else:
            return unit_w_prefix, 'NA'

    def convert_value(self, value, in_unit, out_unit):
        # TODO change conversion to work with combined units (i.e. g/m*s).
        """
        Converts from one unit to another. Only works for set classes (i.e. mass, mol, or temperature)
        :param value: Initial value
        :param in_unit: Unit converting from.
        :param out_unit: Unit converting to.
        :return: Value in new unit.
        """
        if in_unit == out_unit:  # If trying to convert fromm one unit to the same unit, just return value.
            return value
        else:
            aliases = self.get_aliases()
            unit_conv = self.get_units()
            try:
                in_unit = aliases[in_unit]  # Getting unit name from ALIAS.
                out_unit = aliases[out_unit]
                in_conv = unit_conv[in_unit]  # Getting conversion from UNITS.
                out_conv = unit_conv[out_unit]
            except KeyError:
                raise UnitError("Invalid unit entered for {} value.".format(self.__name__))

            new_value = value * (out_conv / in_conv)
            return new_value

    @staticmethod
    def combine_units(self_units, other_units, sign):
        new_units = []
        added_units = []
        print(sign)
        print('self', self_units)
        print('other', other_units)
        for self_base_unit in self_units:  # Loop through unit lists to add orders if in both.
            print('----------')
            for other_base_unit in other_units:
                print(other_base_unit)
                if self_base_unit['dim'] == other_base_unit['dim']:
                    new_order = self_base_unit['order'] + (sign * other_base_unit['order'])
                    print(new_order)
                    new_unit_def = {'dim': self_base_unit['dim'],
                                    'order': new_order,
                                    'prefix': self_base_unit['prefix']}
                    new_units.append(new_unit_def)
                    added_units.append(self_base_unit['dim'])

                # Adds other's units that aren't in both.
                elif (other_base_unit['dim'] not in added_units and not
                      any(base_unit['dim'] == other_base_unit['dim'] for base_unit in self_units)):
                    new_order = sign * other_base_unit['order']
                    new_unit_def = {'dim': other_base_unit['dim'],
                                    'order': new_order,
                                    'prefix': other_base_unit['prefix']}
                    new_units.append(new_unit_def)
                    added_units.append(other_base_unit['dim'])

                print('new unit: ', new_units)
                print('added units: ', added_units)
            if self_base_unit['dim'] not in added_units:  # Adds self's units that aren't in both.
                new_units.append(self_base_unit)
                added_units.append(self_base_unit['dim'])
            print('final-SBU: ', self_base_unit)
        print('comp: ', new_units)
        print('----------')
        nume_count = 0
        for unit_def in new_units:
            if unit_def['order'] > 0:
                nume_count += 1
        if nume_count == 0:
            new_units.append({'dim': 'inverse', 'order': 1, 'prefix': 'NA'})
        print('Final: ',new_units)
        return new_units

    @staticmethod
    def dimensions_present(unit_defs):
        dimension_list = [dimensions['dim'] for dimensions in unit_defs]
        return dimension_list

    @staticmethod
    def rectify_units(unit_defs):
        """
        Remove units from unit def list if they have a zeroth order or have an inverse 1 with other numerators.

        :param unit_defs: Unit def list to check.
        :return: Unit def list with zeroth order units removed.
        """
        numerator_cnt = 0
        inverse_def = 0
        for unit_def in unit_defs:
            if unit_def['dim'] == 'inverse':
                inverse_def = unit_def
            if unit_def['order'] > 0:
                numerator_cnt += 1
            elif unit_def['order'] == 0:
                unit_defs.remove(unit_def)
        if inverse_def in unit_defs and numerator_cnt > 1:
            unit_defs.remove(inverse_def)
        return unit_defs

    @staticmethod
    def has_same_units(unit_defs1, unit_defs2):
        """
        Checks whether two unit_defs lists are the same. May not be in same order so check is necessary. First checks
        list length. If lengths are different, then lists are different and False is returned. If they are the same
        length, then the function runs through list and sees if number of matching defs equals total length.

        There may be a better way of doing this.

        :param unit_defs1: First unit def list to check.
        :param unit_defs2: Second unit def list to check.
        :return: True if the two lists are the same.
        """
        cnt_unit_defs1 = len(unit_defs1)
        cnt_unit_defs2 = len(unit_defs2)
        num_defs = max(cnt_unit_defs1, cnt_unit_defs2)  # Length of longer list for comparison
        if cnt_unit_defs1 != cnt_unit_defs2:
            return False
        same_defs_count = 0
        for unit_def in unit_defs2:
            if unit_def in unit_defs1:
                same_defs_count += 1

        return same_defs_count == num_defs

    @classmethod
    def get_units(cls):
        units = cls.UNITS.copy()
        for unit in cls.SI_UNITS:
            unit_value = units[unit]
            for magnitude, value in cls.SI_MAGNITUDES.items():
                unit_abbreviation = cls.SI_PREFIXES[magnitude] + unit
                units[unit_abbreviation] = unit_value * value
        return units

    @classmethod
    def get_si_aliases(cls):
        si_aliases = {}
        for alias, abbrev in cls.ALIAS.items():
            if abbrev in cls.SI_UNITS:
                si_aliases[alias] = abbrev
        return si_aliases

    @classmethod
    def get_aliases(cls):
        aliases = cls.ALIAS.copy()
        si_aliases = cls.get_si_aliases()
        for si_alias, unit_abbrev in si_aliases.items():
            for magnitude, _ in cls.SI_MAGNITUDES.items():
                magnitude_alias = magnitude + si_alias
                prefix = cls.SI_PREFIXES[magnitude]
                aliases[magnitude_alias] = prefix + unit_abbrev
        return aliases

    # regular arithmetic methods

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise UnitlessNumberError('Can not add a dimensionless value to a value with units.')
        if not self.has_same_units(self.unit_defs, other.unit_defs):
            raise UnitMismatchError('Can not add two numbers with different units.')
        new_value = self.value + other.value
        new_unit_obj = self.__class__(new_value, self.unit_defs)
        return new_unit_obj

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise UnitlessNumberError('Can not subtract a dimensionless value to a value with units.')
        if not self.has_same_units(self.unit_defs, other.unit_defs):
            raise UnitMismatchError('Can not add two numbers with different units.')
        new_value = self.value - other.value
        new_unit_obj = self.__class__(new_value, self.unit_defs)
        return new_unit_obj

    def __mul__(self, other):  # Todo add dimensionless type
        """
        Multiplies two values with units together. When multiplied, the orders of units are added together.
        If other has no units, other is treated as dimensionless and self's units are used.
        :param other: Other value in multiplication.
        :return: New unit having object with multiplied value and combined units.
        """
        if isinstance(other, NUMERICS):
            if implicit_dimensionless:
                new_value = self.value * other
                new_units = self.unit_defs
            else:
                raise UnitlessNumberError("Can not multiply a dimensionless number without explicitly declaring it as "
                                          "one or setting the implicit_dimensionless flag (i.e. implicit_dimensionless "
                                          "= True")

        elif isinstance(other, complex):
            raise NotImplementedError("Complex numbers have not been implemented.")

        elif isinstance(other, self.__class__):
            new_value = self.value * other.value
            new_units = self.combine_units(self.unit_defs, other.unit_defs, 1)

        else:
            raise NotImplementedError("The type of the value you are multiplying by either has not been implemented or "
                                      "is non-numeric.")

        new_units = self.rectify_units(new_units)
        new_unit_obj = self.__class__(new_value, new_units)
        return new_unit_obj

    def __truediv__(self, other):
        """
        Divides one value with units with another. When divided, the orders of denominator's units are subtracted
        from the numerator's. Replaces / operator and returns floats.
        If other has no units, other is treated as dimensionless and self's units are used.
        :param other: Other value in division.
        :return: New unit having object with division value and combined units.
        """
        if isinstance(other, NUMERICS):
            if implicit_dimensionless:
                new_value = self.value / other
                new_units = self.unit_defs
            else:
                raise UnitlessNumberError("Can not divide by a dimensionless number without explicitly declaring it as "
                                          "one or setting the implicit_dimensionless flag (i.e. implicit_dimensionless "
                                          "= True")
        elif isinstance(other, complex):
            raise NotImplementedError("Complex numbers have not been implemented.")

        elif isinstance(other, self.__class__):
            new_value = self.value / other.value
            new_units = self.combine_units(self.unit_defs, other.unit_defs, -1)

        else:
            raise NotImplementedError("The type of the value you are multiplying by either has not been implemented or "
                                      "is non-numeric.")

        new_units = self.rectify_units(new_units)
        new_unit_obj = self.__class__(new_value, new_units)
        return new_unit_obj

    def __floordiv__(self, other):
        """
        Divides one value with units with another and returns the floor of the result. When divided, the orders of
        denominator's units are subtracted from the numerator's. Replaces // operator and returns floats.
        If other has no units, other is treated as dimensionless and self's units are used.
        :param other: Other value in division.
        :return: New unit having object with division value and combined units.
        """
        if isinstance(other, NUMERICS):
            if implicit_dimensionless:
                new_value = self.value // other
                new_units = self.unit_defs
            else:
                raise UnitlessNumberError("Can not divide by a dimensionless number without explicitly declaring it as "
                                          "one or setting the implicit_dimensionless flag (i.e. implicit_dimensionless "
                                          "= True")

        elif isinstance(other, complex):
            raise NotImplementedError("Complex numbers have not been implemented.")

        elif isinstance(other, self.__class__):
            new_value = self.value // other.value

            new_units = self.combine_units(self.unit_defs, other.unit_defs, -1)

        else:
            raise NotImplementedError("The type of the value you are multiplying by either has not been implemented or "
                                      "is non-numeric.")

        new_units = self.rectify_units(new_units)
        new_unit_obj = self.__class__(new_value, new_units)
        return new_unit_obj

    def __mod__(self, other):
        raise NotImplementedError("Mod function has not yet been implemented.")

    def __divmod__(self, other):
        raise NotImplementedError("Divmod function has not yet been implemented.")

    def __pow__(self, power, modulo=None):
        if modulo is not None:
            raise NotImplementedError('Modulo in powers is not supported')

        if not (isinstance(power, NUMERICS) or isinstance(power, complex)):
            raise TypeError("The exponent either is not a numeric type, has not been implemented, or has units, "
                            "which is not allowed.")

        else:
            new_value = self.value ** power
            new_units = []
            for unit_def in self.unit_defs:
                new_order = unit_def['order'] * power
                new_units.append({'dim': unit_def['dim'], 'order': new_order})

            new_units = self.rectify_units(new_units)
            new_unit_obj = self.__class__(new_value, new_units)
            return new_unit_obj

    # augmented arithmetic

    def __iadd__(self, other):
        if not isinstance(other, self.__class__):
            raise UnitlessNumberError('Can not add a dimensionless value to a value with units.')
        if not self.has_same_units(self.unit_defs, other.unit_defs):
            raise UnitMismatchError('Can not add two numbers with different units.')
        self.value += other.value
        return self

    def __isub__(self, other):
        if not isinstance(other, self.__class__):
            raise UnitlessNumberError('Can not subtract a dimensionless value to a value with units.')
        if not self.has_same_units(self.unit_defs, other.unit_defs):
            raise UnitMismatchError('Can not add two numbers with different units.')
        self.value -= other.value
        return self

    def __imul__(self, other):
        """
        Multiplies two values with units together. When multiplied, the orders of units are added together.
        If other has no units, other is treated as dimensionless and self's units are used.
        :param other: Other value in multiplication.
        :return: New unit having object with multiplied value and combined units.
        """
        if isinstance(other, NUMERICS):
            if implicit_dimensionless:
                new_value = self.value * other
                new_units = self.unit_defs
            else:
                raise UnitlessNumberError("Can not multiply a dimensionless number without explicitly declaring it as "
                                          "one or setting the implicit_dimensionless flag (i.e. implicit_dimensionless "
                                          "= True")

        elif isinstance(other, complex):
            raise NotImplementedError("Complex numbers have not been implemented.")

        elif isinstance(other, self.__class__):
            new_value = self.value * other.value
            new_units = self.combine_units(self.unit_defs, other.unit_defs, 1)

        else:
            raise NotImplementedError("The type of the value you are multiplying by either has not been implemented or "
                                      "is non-numeric.")

        new_units = self.rectify_units(new_units)
        self.value = new_value
        self.unit_defs = new_units
        return self

    def __itruediv__(self, other):
        """
        Divides one value with units with another. When divided, the orders of denominator's units are subtracted
        from the numerator's. Replaces / operator and returns floats.
        If other has no units, other is treated as dimensionless and self's units are used.
        :param other: Other value in division.
        :return: New unit having object with division value and combined units.
        """
        if isinstance(other, NUMERICS):
            if implicit_dimensionless:
                new_value = self.value / other
                new_units = self.unit_defs
            else:
                raise UnitlessNumberError("Can not divide by a dimensionless number without explicitly declaring it as "
                                          "one or setting the implicit_dimensionless flag (i.e. implicit_dimensionless "
                                          "= True")

        elif isinstance(other, complex):
            raise NotImplementedError("Complex numbers have not been implemented.")

        elif isinstance(other, self.__class__):
            new_value = self.value / other.value
            new_units = self.combine_units(self.unit_defs, other.unit_defs, -1)

        else:
            raise NotImplementedError("The type of the value you are multiplying by either has not been implemented or "
                                      "is non-numeric.")

        new_units = self.rectify_units(new_units)
        self.value = new_value
        self.unit_defs = new_units
        return self

    def __ifloordiv__(self, other):
        """
        Divides one value with units with another and returns the floor of the result. When divided, the orders of
        denominator's units are subtracted from the numerator's. Replaces // operator and returns floats.
        If other has no units, other is treated as dimensionless and self's units are used.
        :param other: Other value in division.
        :return: New unit having object with division value and combined units.
        """
        if isinstance(other, NUMERICS):
            if implicit_dimensionless:
                new_value = self.value // other
                new_units = self.unit_defs
            else:
                raise UnitlessNumberError("Can not divide by a dimensionless number without explicitly declaring it as "
                                          "one or setting the implicit_dimensionless flag (i.e. implicit_dimensionless "
                                          "= True")

        elif isinstance(other, complex):
            raise NotImplementedError("Complex numbers have not been implemented.")

        elif isinstance(other, self.__class__):
            new_value = self.value // other.value
            new_units = self.combine_units(self.unit_defs, other.unit_defs, -1)

        else:
            raise NotImplementedError("The type of the value you are multiplying by either has not been implemented or "
                                      "is non-numeric.")

        new_units = self.rectify_units(new_units)
        self.value = new_value
        self.unit_defs = new_units
        return self

    def __ipow__(self, power, modulo=None):
        if modulo is not None:
            raise NotImplementedError('Modulo in powers is not supported.')

        if not (isinstance(power, NUMERICS) or isinstance(power, complex)):
            raise TypeError("The exponent either is not a numerical type, has not been implemented, or has units, "
                            "which is not allowed.")

        else:
            new_value = self.value ** power
            new_units = []
            for unit_def in self.unit_defs:
                new_order = unit_def['order'] * power
                new_units.append({'dim': unit_def['dim'], 'order': new_order})

            new_units = self.rectify_units(new_units)
            self.value = new_value
            self.unit_defs = new_units
            return self

    # Unary arithmetic

    def __neg__(self):
        new_value = - self.value
        new_unit_obj = self.__class__(new_value, self.unit_defs)
        return new_unit_obj

    def __pos__(self):
        new_unit_obj = self.__class__(self.value, self.unit_defs)
        return new_unit_obj

    def __abs__(self):
        new_value = abs(self.value)
        new_unit_obj = self.__class__(new_value, self.unit_defs)
        return new_unit_obj

    # Numeric type conversions

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    # Rounding related methods

    def __round__(self, n=None):
        new_value = round(self.value, n)
        new_unit_obj = self.__class__(new_value, self.unit_defs)
        return new_unit_obj

    def __trunc__(self):
        new_value = trunc(self.value)
        new_unit_obj = self.__class__(new_value, self.unit_defs)
        return new_unit_obj

    def __floor__(self):
        new_value = floor(self.value)
        new_unit_obj = self.__class__(new_value, self.unit_defs)
        return new_unit_obj

    def __ceil__(self):
        new_value = ceil(self.value)
        new_unit_obj = self.__class__(new_value, self.unit_defs)
        return new_unit_obj

    # Comparison

    def __lt__(self, other):
        if isinstance(other, self.__class__) and self.has_same_units(self.unit_defs, other.unit_defs):
            return self.value < other.value
        else:  # Return False if different type or unit.
            return False

    def __le__(self, other):
        if isinstance(other, self.__class__) and self.has_same_units(self.unit_defs, other.unit_defs):
            return self.value <= other.value
        else:  # Return False if different type or unit.
            return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.has_same_units(self.unit_defs, other.unit_defs):
                return self.value == other.value
            else:
                return False
        else:  # Return False if different type or unit.
            return False

    # Misc methods

    def __hash__(self):
        return hash((self.value, self.unit_defs))

    def __bool__(self):
        if self.value == 0:
            return False
        else:
            return True

    def __repr__(self):
        if self.frac_format:
            return "{} {}".format(self.value, self.build_unit_string())
        else:
            return "{} {}".format(self.value, self.build_exp_unit_string())

    def __str__(self):
        if self.frac_format:
            return "{} {}".format(self.value, self.build_unit_string())
        else:
            return "{} {}".format(self.value, self.build_exp_unit_string())

    def __getattr__(self, item):  # TODO
        pass
