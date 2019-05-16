from unitpy import BaseUnit

__all__ = [
    'Mass',
    'Weight',
]


class Mass(BaseUnit):
    """
    Class for mass measurements. Contains mass units used in industry and academia.

    Energy measurements can be converted into a mass using the famous mass–energy equivalence formula from Einstein's
    special theory of relativity, E=m*c^2, where E is energy, m is mass, and c is the speed of light.
    """
    STANDARD_UNIT = 'g'
    UNITS = {
        'g': 1.0,
        'tonne': 1000000.0,
        'oz': 28.3495,
        'troy_oz': 3.110348E1,  # Used for precious metals
        'lb': 453.592,
        'short_ton': 907185.0,
        'long_ton': 1016000.0,
        'gr': 0.0647989,
        'stone': 6350.29,  # 14 lbs. used in GB and Ireland for body mass.
        'carat': 0.2,  # Used for gemstones and jewels.
        'solar_mass': 2E33,
        'earth_mass': 5.9722E27,
    }
    ALIAS = {
        'mcg': 'ug',
        'μg': 'ug',
        'gram': 'g',
        'gm': 'g',
        'ton': 'short_ton',
        'short ton': 'short_ton',
        'metric tonne': 'tonne',
        'metric ton': 'tonne',
        'ounce': 'oz',
        'pound': 'lb',
        'lbs': 'lb',
        'slug': 'lb',
        'st': 'stone',
        'long ton': 'long_ton',
        'weight ton': 'long_ton',
        'imperial ton': 'long_ton',
        'imp_ton': 'long_ton',
        'ct': 'carat',
        'sm': 'solar_mass',
        'suns': 'solar_mass',
        'em': 'earth_mass',
        'earths': 'earth_mass',

    }
    SI_UNITS = ['g']

    def __init__(self, value, unit):
        self.init_value = value
        self.in_unit = unit
        self.base_unit = 'A'
        base_value = self.convert_value(self.init_value, self.in_unit, self.base_unit )
        super(self.__class__, self).__init__(base_value, self.base_unit)

# For backward compatibility
Weight = Mass
