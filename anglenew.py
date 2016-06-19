"""
ISSUES:
1. [SOLVED] max number of supported variables is not known, refer to self.dimension_support in __init__
2. Exceptions in __init__, and other various places are too general, make them more specific?
3. [SOLVED] in __add__, check if other.coefficients == self.coefficients
4. [SOLVED] in __add__, make Angle addable to int and vice versa
5. Float numbers are not supported in __add__, etc
6. Angle relationships are not supported. G.e. a+b+c+d=240;
7. Angle.__init__: passed parameter coefficients is not checked for type of data

NOTES:
"""

__author__ = 'satbek'

# allows support for up to len(GREEK_LETTERS) variables
GREEK_LETTERS = 'αβγδεηθλπρστμφω'
VAR_SUPPORT = len('αβγδεηθλπρστμφω')

# total of 24 letters
GREEK_LETTER_NAMES = {'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta',
                      'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi',
                      'ο': 'omicron', 'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi',
                      'χ': 'chi', 'ψ': 'psi', 'ω': 'omega'}


class Angle:
    """
    INTENT:
    Defines an angle in terms of a list of integer/float numbers. Allows to work with variable angles.
    G.e. Let's say the angle is: aα + bβ + c, where α and β are variables.
    Then, this angle can be expressed by [a, b, c] a.k.a. coefficients.

    IMPORTANT:
    1. This class supports up to 15 variables.
    2. If all of self.coefficients are 0, then the angle is said to be unknown.
    """

    def __init__(self, coefficients):
        """
        PRE1: len(coefficients) >= 1
        PRE2: len(coefficients) <= self.dimension_support

        """

        # PRE1
        if len(coefficients) < 1:
            error_msg = 'Angle: you need to provide at least one coefficient.'
            raise Exception(error_msg)

        # PRE2
        if len(coefficients) > VAR_SUPPORT:
            error_msg = 'Angle: this class supports {} variables. You provided too many ({}) variables.'
            raise Exception(error_msg.format(VAR_SUPPORT, len(coefficients)))

        self.coefficients = coefficients

    def __add__(self, other):
        """
        INTENT:
        Performs addition of Angle objects.

        PRE1: other is instance of Angle or int
        PRE2: if other is Angle, 
        """

        # PRE1
        if not isinstance(other, Angle) and not isinstance(other, int):
            error_msg = 'Angle: Trying to add {} object to an Angle object. Angle or int is required.'
            raise TypeError(error_msg.format(str(type(other))[8:-2]))

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
        result = ''
        for i in range(len(self.coefficients) - 1):
            a = self.coefficients[i]
            if a > 0:
                result += ' + ' + str(a) if a != 1 else '' + GREEK_LETTERS[i]
            elif a < 0:
                result += ' - ' + str(abs(a)) + GREEK_LETTERS[i]

        a = self.coefficients[-1]

        if a > 0:
            result += ' + ' + str(a)
        elif a < 0:
            result += ' - ' + str(abs(a))

        if result[:3] == ' - ':
            result = '-' + result[3:]
        elif result[:3] == ' + ':
            result = result[3:]

        return result

    def __hash__(self):
        rtrn_str = ''
        for c in self.coefficients:
            rtrn_str += str(c)
        return hash(rtrn_str)

    def get_coefficients(self):
        return self.coefficients

    def get_dimension(self):
        return len(self.coefficients)

    def get_angle_180(self):
        # returns 180 degree angle of dimension as self
        angle = [0] * (self.get_dimension() - 1) + [180]
        return Angle(angle)

    def get_angle_360(self):
        # returns 360 degree angle of dimension as self
        angle = [0] * (self.get_dimension() - 1) + [360]
        return Angle(angle)

    def is_known(self):
        for c in self.coefficients:
            if c != 0:
                return True
        return False

    @classmethod
    def from_str(cls, a_str, dimension):
        if a_str == 'x':
            return Angle([0] * dimension)

        nums = list(map(float, a_str.split()))
        if len(nums) != dimension:
            raise Exception('R u kidding me?!')

        return Angle(nums)
