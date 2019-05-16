from unitpy import BaseUnit
from mpmath import mpf

#implicit_dimensionless = True



#single_unit = {'dim': '?', 'order': 1}

#viscosity = [{'dim': 'M', 'order': 1}, {'dim': 'L', 'order': -1}, {'dim': 'T', 'order': -1}]

#diff_coeff = [{'dim': 'M', 'order': 2}, {'dim': 'T', 'order': -1}]
#conc_grad = [{'dim': 'N', 'order': 1}, {'dim': 'M', 'order': -4}]
#diff_coeff = 'm/s'
#conc_grad = 'mol/m^4'

#diff = BaseUnit(2, diff_coeff)
#conc = BaseUnit(3, conc_grad)

#temp = diff * conc
#print(temp)

#temp *= 2
#print(temp)

#temp **= 2

#print(temp)

t = mpf(5/9)

x = BaseUnit(t, 'm/s')
y = BaseUnit(4, 'm')
z = x * y
print(z)
