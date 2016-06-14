"""
ISSUES:
1. How many variables should it support? refer to self.dimension_support in __init__
2. Exceptions in __init__ are too general, make them more specific?
3. [SOLVED] in __add__, check if other.coefficients == self.coefficients
4. [SOLVED] in __add__, make Angle addable to int and vice versa

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
        len(coefficients) >= 1 AND len(coefficients) <= self.dimension_support

        """
        self.dimension_support = len(GREEK_LETTERS)

        if len(coefficients) < 1:
            error_msg = 'From class Angle: you need to provide at least one element in coefficients.'
            raise Exception(error_msg)

        if len(coefficients) > self.dimension_support:
            error_msg = 'From class Angle: this class supports {} variables. You provided {} variables.'
            raise Exception(error_msg.format(self.dimension_support, len(coefficients)))

        self.coefficients = coefficients

    def __add__(self, other):
        if not isinstance(other, Angle) and not isinstance(other, int):
            error_msg = 'Trying to add non-Angle or non-int object to an Angle object.'
            raise TypeError(error_msg)

        if isinstance(other, Angle) and len(self.coefficients) != len(other.coefficients):
            error_msg = 'From Angle.__add__, coefficients in both addends have to contain same number of variables.'
            raise Exception(error_msg)

        if isinstance(other, int):
            other_angle = [0] * (len(self.coefficients) - 1) + [other]
            return Angle(list(map(sum, zip(self.coefficients, other_angle))))

        return Angle(list(map(sum, zip(self.coefficients, other.coefficients))))

    def __radd__(self, other):
        if not isinstance(other, int):
            error_msg = 'Trying to add Angle object to a non-int object.'
            raise TypeError(error_msg)

        other_angle = [0] * (len(self.coefficients) - 1) + [other]

        return self + Angle(other_angle)

    def __sub__(self, other):
        if not isinstance(other, Angle) and not isinstance(other, int):
            error_msg = 'Trying to subtract non-Angle or non-int object from an Angle object.'
            raise TypeError(error_msg)

        if isinstance(other, Angle):
            other_angle = list(map(lambda x: -x, other.coefficients))
            return self + Angle(other_angle)

        other_angle = [0] * (len(self.coefficients) - 1) + [-other]

        return self + Angle(other_angle)

    def __rsub__(self, other):
        if not isinstance(other, int):
            error_msg = 'Trying to subtract Angle object from a non-int object.'
            raise TypeError(error_msg)

        other_angle = list(map(lambda x: -x, self.coefficients))
        return Angle(other_angle) + other

    def __floordiv__(self, other):
        if not isinstance(other, int):
            raise TypeError('Trying to floor-div an Angle object by a non-int value.')

        other_angle = list(map(lambda x: x // other, self.coefficients))
        return Angle(other_angle)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError('Trying to multiply an Angle object to a non-int value.')

        other_angle = list(map(lambda x: x * other, self.coefficients))
        return Angle(other_angle)

    def __rmul__(self, other):
        if not isinstance(other, int):
            raise TypeError('Trying to multiply an Angle object to a non-int value.')

        return self * other

    def __eq__(self, other):
        if len(self.coefficients) != len(other.coefficients):
            raise Exception('Trying to compare two Angle objects of different dimension.')

        for i in range(len(self.coefficients)):
            if self.coefficients[i] != other.coefficients[i]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        rtrn_str = ''
        for i in range(len(self.coefficients) - 1):
            rtrn_str += str(self.coefficients[i])
            rtrn_str += GREEK_LETTERS[i] + ' '
        rtrn_str += str(self.coefficients[-1])
        return rtrn_str

    def __hash__(self):
        rtrn_str = ''
        for c in self.coefficients:
            rtrn_str += str(c)
        return hash(rtrn_str)

    def get_coefficients(self):
        return self.coefficients

    def is_known(self):
        for c in self.coefficients:
            if c != 0:
                return True
        return False

    @classmethod
    def from_str(cls, a_str):
        pass

a = Angle([1,2,3,4,5,60])
b = Angle([2,3,4,5,6,70])
print(a-b)