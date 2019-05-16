from unitpy import BaseUnit

__all__ = [
    'Current'
]


class Current(BaseUnit):
    STANDARD_UNIT = 'A'
    UNITS = {
        'A': 1.0,
    }
    ALIAS = {
        'amp': 'A',
        'ampere': 'A',
    }
    SI_UNITS = ['A']

    def __init__(self, value, unit):
        self.init_value = value
        self.in_unit = unit
        self.base_unit = 'A'
        base_value = self.convert_value(self.init_value, self.in_unit, self.base_unit )
        super(Current, self).__init__(base_value, self.base_unit)
