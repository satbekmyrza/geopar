"""
ISSUES:
1. How many variables should it support? refer to self.support_num_var in __init__
2. Exceptions in __init__ to general
3. in __add__, check if other.coefficients == self.coefficients [SOLVED]

NOTES:
"""

__author__ = 'satbek'

# allows support for up to len(GREEK_LETTERS) variables
GREEK_LETTERS = 'αβγδεηθλπρστμφω'

# total of 24 letters
GREEK_LETTER_NAMES = {'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta',
                      'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi',
                      'ο': 'omicron', 'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi',
                      'χ': 'chi', 'ψ': 'psi', 'ω': 'omega'}


class Angle:
    def __init__(self, coefficients):
        """
        PRE1:
        len(coefficients) >= 1 AND len(coefficients) <= self.support_num_var

        """
        self.support_num_var = len(GREEK_LETTERS)

        if len(coefficients) < 1:
            raise Exception('From class Angle: you need to provide at least one element in coefficients.')

        if len(coefficients) > self.support_num_var:
            error_msg = 'From class Angle: this class supports {} variables. You provided too many variables.'
            raise Exception(error_msg.format(self.support_num_var))

        self.coefficients = coefficients

    def __add__(self, other):
        if not isinstance(other, Angle):
            raise TypeError('You cannot add non-Angle object to an Angle object.')

        if len(self.coefficients) != len(other.coefficients):
            raise Exception('From Angle.__add__, coefficients in both addends should be of same magnitude.')

        return Angle(list(map(sum, zip(self.coefficients, other.coefficients))))

a = Angle([1,2,3,4,5,6])
b = Angle([2,3,4,5,6,7])
a+b