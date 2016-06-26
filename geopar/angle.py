from fractions import Fraction

"""
ISSUES:
1. [SOLVED] max number of supported variables is not known, refer to self.dimension_support in __init__
2. Exceptions in __init__, and other various places are too general, make them more specific?
3. [SOLVED] in __add__, check if other.coefficients == self.coefficients
4. [SOLVED] in __add__, make Angle addable to int and vice versa
5. Float numbers are not supported in __add__, etc
6. Angle relationships are not supported. G.e. a+b+c+d=240;
7. Angle.__init__: passed parameter coefficients is not checked for type of data
8. [SOLVED] Angle: __truediv__ is not implemented
9. Unknown Angle object has a dimension. Not necessary.
10. [SOLVED] __str__ does not process unknown angle

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
        Performs addition of two Angle objects.

        PRE1: other is instance of Angle or int
        PRE2: if other is Angle, then self.get_dimension() == other.get_dimension()
        """

        # PRE1
        if not isinstance(other, Angle) and not isinstance(other, int):
            error_msg = 'Angle: Trying to add {} object to an Angle object. Angle or int is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        # PRE2
        if isinstance(other, Angle) and self.get_dimension() != other.get_dimension():
            error_msg = 'Angle: both addends should have the same dimension! {} != {}'
            raise Exception(error_msg.format(self.get_dimension(), other.get_dimension()))

        if isinstance(other, int):
            other_angle = [Fraction(0)] * (self.get_dimension() - 1) + [Fraction(other)]
            return self + Angle(other_angle)

        return Angle(list(map(sum, zip(self.coefficients, other.coefficients))))

    def __radd__(self, other):
        """
        INTENT:
        Performs addition of two Angle objects.

        PRE1: other is instance of int
        """

        # PRE1
        if not isinstance(other, int):
            error_msg = 'Angle: Trying to add Angle object to {} object. int is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        other_angle = [Fraction(0)] * (len(self.coefficients) - 1) + [Fraction(other)]

        return self + Angle(other_angle)

    def __sub__(self, other):
        """
        INTENT:
        Performs subtraction of two Angle objects.

        PRE1: other is instance of Angle or int
        PRE2: if other is Angle, then self.get_dimension() == other.get_dimension()
        """

        # PRE1
        if not isinstance(other, Angle) and not isinstance(other, int):
            error_msg = 'Angle: Trying to subtract {} object from an Angle object. Angle or int is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        # PRE2
        if isinstance(other, Angle) and self.get_dimension() != other.get_dimension():
            error_msg = 'Angle: minuend and subtrahend should have the same dimension! {} != {}'
            raise Exception(error_msg.format(self.get_dimension(), other.get_dimension()))

        other_angle = None
        if isinstance(other, int):
            other_angle = [Fraction(0)] * (len(self.coefficients) - 1) + [Fraction(-other)]
        elif isinstance(other, Angle):
            other_angle = list(map(lambda x: -x, other.coefficients))

        return self + Angle(other_angle)

    def __rsub__(self, other):
        """
        INTENT:
        Performs subtraction of two Angle objects.

        PRE1: other is instance of int
        """

        # PRE1
        if not isinstance(other, int):
            error_msg = 'Angle: Trying to subtract Angle object from a {} object. int is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        other_angle = list(map(lambda x: -x, self.coefficients))
        return Angle(other_angle) + other

    def __truediv__(self, other):
        """
        INTENT:
        Performs a floor division of Angle by other

        PRE1:
        other is instance of int
        """

        # PRE1
        if not isinstance(other, int):
            error_msg = 'Angle: Trying to floor-div an Angle object by a {} object. int is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        other_angle = list(map(lambda x: x / other, self.coefficients))
        return Angle(other_angle)

    def __mul__(self, other):
        """
        INTENT:
        Performs multiplication of Angle object to int

        PRE1:
        other is instance of int
        """

        # PRE1
        if not isinstance(other, int):
            error_msg = 'Angle: Trying to multiply an Angle object to a {} object. int is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        other_angle = list(map(lambda x: x * other, self.coefficients))
        return Angle(other_angle)

    def __rmul__(self, other):
        """
        INTENT:
        Performs multiplication of Angle object to int

        PRE1:
        other is instance of int
        """

        # PRE1
        if not isinstance(other, int):
            error_msg = 'Angle: Trying to multiply an Angle object to a {} object. int is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        return self * other

    def __eq__(self, other):
        """
        INTENT:
        Performs comparison of two Angle objects

        PRE1: other is instance of Angle
        PRE2: if other is Angle, dimensions of other and self are equal
        """

        # PRE1
        if not isinstance(other, Angle):
            error_msg = 'Angle: Trying to compare {} object to Angle object. Angle is required.'
            raise Exception(error_msg.format(type(other).__name__))

        # PRE2
        if len(self.coefficients) != len(other.coefficients):
            error_msg = 'Angle: Trying to compare two Angle objects of different dimension.'
            raise Exception(error_msg)

        for i in range(len(self.coefficients)):
            if self.coefficients[i] != other.coefficients[i]:
                return False

        return True

    def __ne__(self, other):
        """
        INTENT:
        Performs comparison of two Angle objects
        """

        return not self.__eq__(other)

    def __str__(self):
        """
        INTENT:
        Returns string representation of an Angle object
        """

        # processing unknown angle
        if not self.is_known():
            return 'x'

        # prepares first n-1 coefficients
        result = ''
        for i in range(len(self.coefficients) - 1):
            a = self.coefficients[i]
            if a > 0:
                result += (' + ' + str(a) if a != 1 else ' + ') + GREEK_LETTERS[i]
            elif a < 0:
                result += (' - ' + str(abs(a)) if abs(a) != 1 else ' - ') + GREEK_LETTERS[i]

        # prepares the last coefficient
        a = self.coefficients[-1]
        if a > 0:
            result += ' + ' + str(a)
        elif a < 0:
            result += ' - ' + str(abs(a))

        # restoring the sign before the first coefficient
        if result[:3] == ' - ':
            result = '-' + result[3:]
        elif result[:3] == ' + ':
            result = result[3:]

        return result

    def __hash__(self):
        """
        INTENT
        User defined objects in Python are mutable by default. Overriding this method enables to make them immutable.
        This method is specifically written to be able to:
        1. compare two sets of Angle objects with each other.
        2. using collections.Counter for comparing two lists of Angle objects
        Both Python sets and collections.Counter require objects to be hashable.
        """

        # relies on coefficients
        result = ''
        for c in self.coefficients:
            result += str(c)
        return hash(result)

    def get_coefficients(self):
        return self.coefficients

    def get_dimension(self):
        return len(self.coefficients)

    def get_angle_180(self):
        """
        INTENT:
        returns an Angle [0, 0, ..., 0, 180] of dimension as self
        """

        angle = [Fraction(0)] * (self.get_dimension() - 1) + [Fraction(180)]
        return Angle(angle)

    def get_angle_360(self):
        """
        INTENT:
        returns an Angle [0, 0, ..., 0, 360] of dimension as self
        """

        angle = [Fraction(0)] * (self.get_dimension() - 1) + [Fraction(360)]
        return Angle(angle)

    def is_known(self):
        # INTENT
        # enables the user to know whether the value of self is known

        for c in self.coefficients:
            if c != 0:
                return True
        return False

    @classmethod
    def from_str(cls, a_str, a_dimension):
        """
        INTENT
        This is a special class method, which allows to instantiate an Angle object
        of dimension a_dimension from a string value.

        USAGE
        a = Angle.from_str('x', 4)
        print(a.get_coefficients())  # [0, 0, 0, 0]
        b = Angle.from_str('1 0 90', 3)
        print(b)  # α + 90
        c = Angle.from_str('r 1 90', 3)  # ERROR! r is a letter

        PRE
        a_str should be in the form:
            'x' for unknown OR
            'a b c'--where a, b and c are integer numbers--for aα + bβ + c
        """

        if a_str == 'x':
            return Angle([Fraction(0)] * a_dimension)

        nums = list(map(lambda x: Fraction(x), a_str.split()))
        if len(nums) != a_dimension:
            error_msg = 'Angle: provided dimension ({}) is not in correspondence with the angle provided: {}'
            raise Exception(error_msg.format(a_dimension, a_str))

        return Angle(nums)
