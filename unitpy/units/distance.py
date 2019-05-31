# Copyright (c) 2007, Robert Coup <robert.coup@onetrackmind.co.nz>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of Distance nor the names of its contributors may be used
#      to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""
Distance and Area objects to allow for sensible and convenient calculation
and conversions.

Authors: Robert Coup, Justin Bronn, Riccardo Di Virgilio

Inspired by GeoPy (http://exogen.case.edu/projects/geopy/)
and Geoff Biggs' PhD work on dimensioned units for robotics.
"""
#from measurement.base import MeasureBase, NUMERIC_TYPES, pretty_name
from unitpy import BaseUnit


__all__ = ['Distance']


class Distance(BaseUnit):
    STANDARD_UNIT = "m"
    UNITS = {
        'chain': 20.1168,
        'chain_benoit': 20.116782,
        'chain_sears': 20.1167645,
        'british_chain_benoit': 20.1167824944,
        'british_chain_sears': 20.1167651216,
        'british_chain_sears_truncated': 20.116756,
        'british_ft': 0.304799471539,
        'british_yd': 0.914398414616,
        'clarke_ft': 0.3047972654,
        'clarke_link': 0.201166195164,
        'fathom':  1.8288,
        'ft': 0.3048,
        'german_m': 1.0000135965,
        'gold_coast_ft': 0.304799710181508,
        'indian_yd': 0.914398530744,
        'inch': 0.0254,
        'link': 0.201168,
        'link_benoit': 0.20116782,
        'link_sears': 0.20116765,
        'm': 1.0,
        'mi': 1609.344,
        'naut_mi': 1852,
        'naut_mi_uk': 1853.184,
        'rod': 5.029210,
        'sears_yd': 0.91439841,
        'survey_ft': 0.304800609601,
        'yd': 0.9144,
        'ly': 9.46073E15,
        'pc': 3.085678E16,
        'lm': 1.799E10,
        'ls': 2.998E8,
        'ang': 1E-10,
        'au': 1.495979E11,
        'fermi': 1E-15,
    }
    SI_UNITS = [
        'm'
    ]

    # Unit aliases for `UNIT` terms encountered in Spatial Reference WKT.
    ALIAS = {
        'foot': 'ft',
        'inches': 'inch',
        'in': 'inch',
        'meter': 'm',
        'metre': 'm',
        'mile': 'mi',
        'yard': 'yd',
        'british chain (benoit 1895 b)': 'british_chain_benoit',
        'british chain 1895': 'british_chain_benoit',
        'british chain (sears 1922)': 'british_chain_sears',
        'british chain 1922': 'british_chain_sears',
        'british chain 1922 trunc': 'british_chain_sears_truncated',
        'british chain': 'british_chain_sears_truncated',
        'british foot (sears 1922)': 'british_ft',
        'british foot 1922': 'british_ft',
        'british foot': 'british_ft',
        'british yard (sears 1922)': 'british_yd',
        'british yard': 'british_yd',
        "clarke's foot": 'clarke_ft',
        "clarke's link": 'clarke_link',
        'chain (benoit)': 'chain_benoit',
        'chain (sears)': 'chain_sears',
        'foot (international)': 'ft',
        'german legal metre': 'german_m',
        'gold coast foot': 'gold_coast_ft',
        'link (benoit)': 'link_benoit',
        'link (sears)': 'link_sears',
        'nautical mile': 'naut_mi',
        'nautical mile (uk)': 'naut_mi_uk',
        'us survey foot': 'survey_ft',
        'u.s. foot': 'survey_ft',
        'yard (indian)': 'indian_yd',
        'indian yard': 'indian_yd',
        'yard (sears)': 'sears_yd',
        'sears yard': 'sears_yd',
        'light year': 'ly',
        'light-year': 'ly',
        'l.y.': 'ly',
        'parsec': 'pc',
        'light-minute': 'lm',
        'light minute': 'lm',
        'l.m.': 'lm',
        'light-second': 'ls',
        'light second': 'ls',
        'l.s.': 'ls',
        'angstrom': 'ang',
        'ångström': 'ang',

    }

    def __init__(self, in_value, unit):
        value
        super().__init__()

    """def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Area(
                default_unit=AREA_PREFIX + self._default_unit,
                **{
                    AREA_PREFIX + self.STANDARD_UNIT: (
                        self.standard * other.standard
                    )
                }
            )
        elif isinstance(other, NUMERIC_TYPES):
            return self.__class__(
                default_unit=self._default_unit,
                **{self.STANDARD_UNIT: (self.standard * other)}
            )
        else:
            raise TypeError(
                '%(dst)s must be multiplied with number or %(dst)s' % {
                    "dst": pretty_name(self.__class__),
                }
            )"""
