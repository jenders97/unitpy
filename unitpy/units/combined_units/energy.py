from measurement.base import MeasureBase


__all__ = [
    'Energy'
]


class Energy(MeasureBase):
    """
    Class for energy measurements. Contains a number of frequently and infrequently used units for energy from academics
    and industry.

    Electronvolts use the NIST standard conversion where 1 eV = 1.602 176 6208*10^−19 J, with an uncertainty of
    0.000 000 0098*10^-19. https://physics.nist.gov/cgi-bin/cuu/Value?tevj

    Hartrees use the conversion suggested by the 2014 CODATA where 1 hartree = 4.359 744 650*10^−18 J, with an
    uncertainty of 0.000 000 000 54*10^-18 J. https://physics.nist.gov/cgi-bin/cuu/Value?hr

    As the energy of a wave is based solely on its frequency, light's frequency can be used as an energy measurement for
    energy in monochromatic light when multiplied by thePlanck constant (e.g. E=hf). This conversion uses the
    standardized value of h (h = 6.626 070 15*10^-34 J*s) by the CGPM in 2018.
    https://www.bipm.org/utils/common/pdf/CGPM-2018/26th-CGPM-Resolutions.pdf

    Volumes of natural gas are occasionally used as a energy unit in the chemical industry as in a burner or boiler the
    volumetric flow of natural gas correlates to the heat released. The values used were taken from the US annual
    average heat content of natural gas. https://www.eia.gov/tools/faqs/faq.php?id=45&t=8
    https://www.eia.gov/totalenergy/data/monthly/pdf/sec13_4.pdf

    TNT equivalents are often used for explosions or for very large amounts of energy. The typical unit is the metric
    ton of tnt (trinitrotoluene), which is a frequently used traditional explosive compound.
    https://www.nist.gov/pml/nist-guide-si-appendix-b9-factors-units-listed-kind-quantity-or-field-science#ENERGY

    The therm is an energy unit based on the energy released from burning 100 ft3 (2.83 m3) of natural gas. European and
    American standards groups use slightly different conversions from therm to joule.
    https://www.nist.gov/pml/nist-guide-si-appendix-b9-factors-units-listed-kind-quantity-or-field-science#ENERGY

    BTU is a unit based on the energy required to raise the temperature of one pound of water by one degree Fahrenheit.
    There are several different conversions for BTU, based on what temperature the test was run at. The International
    Steam Table Conference value for the BTU (the IT BTU or btu_it) has been divorced from water's properties. The ISO
    version (btu_iso) rounds the IT value to a reasonable number of decimals (ISO 31-4). The thermochemical BTU (btu_th)
    is based off of the thermochemical definition of the calorie.
    Using 'btu' as your unit will automatically use the ISO definition.
    https://www.nist.gov/pml/nist-guide-si-appendix-b9-factors-units-listed-kind-quantity-or-field-science#ENERGY

    The calorie is a unit based on the energy required to raise the temperature of one kg of water by one degree
    celsius. The IT calorie (cal_it) has the same roots as the IT BTU. The thermochemical calorie (cal_th) was defined
    as 4.1833 J due to issues with the value of water's head capacity and and will be used as the default for 'cal'.
    https://www.nist.gov/pml/nist-guide-si-appendix-b9-factors-units-listed-kind-quantity-or-field-science#ENERGY

    The kilocalorie (cal_nutrition) , aka Calorie, is 1000 calories and is often used for the energy content of food.


    """
    STANDARD_UNIT = 'J'
    UNITS = {
        'J': 1.0,
        'foot_pound': 1.355818,
        'foot_poundal': 0.0421401100938048,  # Old energy unit
        'watt_hour': 3600.0,
        'watt_min': 60.0,
        'eV': 1.6021766208E-19,
        'hartree': 4.359744650E-18,
        'erg': 1.0E-7,
        'hertz': 6.62607015E-34,  # Planck's constant J*s.
        'm3_ng': 38637896.84,  # J/m3 of nat gas using
        'cm3_ng': 38.63753164,  # J/cm3 of nat gas.
        'ft3_ng': 1094093.072,  # J/ft3 of natural gas.
        'in3_ng': 633.155713,  # J/in3 of nat gas.
        'tonne_tnt': 4.184E9,
        'therm_ec': 1.05506E8,
        'therm_us': 1.054804E8,
        'btu_it': 1.055055853,
        'btu_iso': 1.05506E3,
        'btu_th': 1.054350E3,
        'btu_mean': 1.05587E3,
        'btu_39': 1.05967E3,  # BTU conversion at 39°F. Maximum density of water.
        'btu_59': 1.05480E3,  # BTU conversion at 59°F. Used for Natural gas pricing in US.
        'btu_60': 1.05468E3,  # BTU conversion at 60°F. Used mostly in Canada.
        'cal_th': 4.184,
        'cal_it': 4.1868,
        'cal_mean': 4.19002,  # Average value of the calorie
        'cal_15': 4.18580,  # Value of the calorie at 15°C.
        'cal_20': 4.18190,  # Value of the calorie at 20°C.
        'cal_nutrition': 4184.0,  # Thermochemical Kcal. May be unneeded.
    }
    ALIAS = {
        'joule': 'J',
        'j': 'J',
        'ftlb': 'foot_pound',
        'ft-lb': 'foot_pound',
        'ft_lb': 'foot_pound',
        'ftlbs': 'foot_pound',
        'ft-lbs': 'foot_pound',
        'ft_lbs': 'foot_pound',
        'ftlbf': 'foot_pound',
        'ft-lbf': 'foot_pound',
        'ft_lbf': 'foot_pound',
        'ft_pdl': 'foot_poundal',
        'ft-pdl': 'foot_poundal',
        'ftpdl': 'foot_poundal',
        'watt_hr': 'watt_hour',
        'watt_h': 'watt_hour',
        'watt_min': 'watt_min',
        'watt_minute': 'watt_min',
        'watt_sec': 'J',
        'watt_s': 'J',
        'ev': 'eV',
        'electronvolt': 'eV',
        'ha': 'hartree',
        'hz': 'hertz',
        'ton_tnt': 'tonne_tnt',
        'tontnt': 'tonne_tnt',
        'tons_tnt': 'tonne_tnt',
        'tonstnt': 'tonne_tnt',
        'tnt': 'tonne_tnt',
        'british_thermal_unit': 'btu',
        'BTU': 'btu',
        'cal': 'cal_th',
        'calorie': 'cal_th',
        'Calorie': 'cal_nutrition',
        'Cal': 'cal_nutrition',
    }
    SI_UNITS = ['J', 'c', 'eV', 'tonne_tnt']
