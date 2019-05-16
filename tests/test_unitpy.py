from unitpy.base_unit import BaseUnit


def test_correct_addition():
    val1 = 10
    val2 = 25.5
    unit = 'kg^3/m*s'
    unit_exp = 'kg^3*m^-1*s^-1'
    obj1 = BaseUnit(val1, unit)
    obj2 = BaseUnit(val2, unit)
    sum_obj = obj1 + obj2
    assert sum_obj.value == (
            val1 + val2) and sum_obj.build_unit_string() == unit and sum_obj.build_exp_unit_string() == unit_exp


def test_correct_sub():
    val1 = 10
    val2 = 25.5
    unit = 'kg^3/m*s'
    unit_exp = 'kg^3*m^-1*s^-1'
    obj1 = BaseUnit(val1, unit)
    obj2 = BaseUnit(val2, unit)
    sum_obj = obj1 - obj2
    assert sum_obj.value == (
            val1 - val2) and sum_obj.build_unit_string() == unit and sum_obj.build_exp_unit_string() == unit_exp


def test_correct_mult():
    val1 = 10
    val2 = 25.5
    unit = 'kg/m^3'
    unit2 = 'm^3/s'
    end_unit = 'kg/s'
    obj1 = BaseUnit(val1, unit)
    obj2 = BaseUnit(val2, unit2)
    sum_obj = obj1 * obj2
    assert sum_obj.value == (
            val1 * val2) and sum_obj.build_unit_string() == end_unit


def test_correct_truediv():
    val1 = 10
    val2 = 25.5
    unit = 'kg/m^3'
    unit2 = 'm^3/s'
    end_unit = 'kg*s/m^6'
    obj1 = BaseUnit(val1, unit)
    obj2 = BaseUnit(val2, unit2)
    sum_obj = obj1 / obj2
    assert sum_obj.value == (
            val1 / val2) and sum_obj.build_unit_string() == end_unit


def test_correct_floordiv():
    val1 = 10
    val2 = 25.5
    unit = 'kg/m^3'
    unit2 = 'm^3/s'
    end_unit = 'kg*s/m^6'
    obj1 = BaseUnit(val1, unit)
    obj2 = BaseUnit(val2, unit2)
    sum_obj = obj1 // obj2
    assert sum_obj.value == (
            val1 // val2) and sum_obj.build_unit_string() == end_unit


