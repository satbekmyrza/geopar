from fractions import Fraction
from decimal import Decimal
import numbers

"""
ISSUES:

SUGGESTIONS:

NOTES:

"""

__author__ = 'satbek'

# allows support for up to len(GREEK_LETTERS) variables (currently 15)
GREEK_LETTERS = 'αβγδεηθλπρστμφω'


class Angle:
    """
    INTENT:
    Defines a geometrical angle in terms of a list of Fraction numbers - _coefficients.

    NOTES:
    _coefficients contains n elements, where 0 <= n <= len(GREEK_LETTERS) + 1.
    Below are different cases for n. When {{1}}:
    1. n == 0, the angle is unknown.
    2. n == 1, the angle is constant.
       _coefficients = [90] --> 90 degrees
       _coefficients = [-30] --> -30 degrees
    3. n == 2, the angle has one variable (first letter of GREEK_LETTERS) and a constant term.
       _coefficients = [1, 45] --> α + 45
       _coefficients = [-1, -30] --> -α - 30
       _coefficients = [-1, 0] --> -α
    4. n == 3, the angle has two variables (first two letters of GREEK_LETTERS) and a constant term.
       _coefficients = [1, 1, 30] --> α + β + 30
       _coefficients = [0, -1, 30] --> -β + 30
       _coefficients = [-1, -1, 120] --> -α - β + 120
       _coefficients = [1, 1, 0] --> α + β
    ... and so on.

    The angle can be in either of two states: known or unknown.
    If len(_coefficients) == 0, then the angle is said to be unknown.
    Otherwise, the angle is said to be known.

    {{1}} To explain more easily, I used integers as coefficients. However, keep in mind that _coefficients
    contains ONLY objects of built-in Fraction class.
    """

    def __init__(self, _coefficients):
        """
        PRE1: len(_coefficients) <= len(GREEK_LETTERS) + 1
        PRE2: _coefficients[i] is an instance of Fraction, where 0 <= i < len(_coefficients)
        """

        # PRE1
        if len(_coefficients) > len(GREEK_LETTERS) + 1:
            raise Exception('Too many coefficients were provided.')

        # PRE2
        for coef in _coefficients:
            if not (isinstance(coef, Fraction)):
                raise Exception('Coefficient provided is not Fraction.')

        self._coefficients = _coefficients

    def __add__(self, other):
        """
        Implements binary arithmetic operation '+'.

        PRE1: other is instance of Angle, int, or float
        PRE2: if other is instance Angle, then:
                1. self.get_dimension() == other.get_dimension()
                2. other is known
        """

        # PRE1
        if not (isinstance(other, Angle) or isinstance(other, int) or isinstance(other, float)):
            raise Exception('Wrong type provided.')

        # PRE2
        if isinstance(other, Angle):
            if self.get_dimension() != other.get_dimension():
                raise Exception('Angles to be added have different dimensions.')
            if not other.is_known():
                raise Exception('Angle to be added is unknown.')

        # int, float
        if isinstance(other, int) or isinstance(other, float):
            other_angle = [Fraction(0)] * (self.get_dimension() - 1) + [Fraction(Decimal(str(other)))]
            return self + Angle(other_angle)

        # Angle
        return Angle(list(map(sum, zip(self._coefficients, other.get_coefficients()))))

    def __radd__(self, other):
        """
        INTENT:
        Performs addition:
          numbers.Real + Angle

        PRE1: other is instance of numbers.Real
        PRE2: if other is Angle, then self.get_dimension() == other.get_dimension()
        """

        # PRE1
        if not isinstance(other, numbers.Real):
            error_msg = 'Angle: Trying to add Angle object to <{}> object. int or float is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        other_angle = [Fraction(0)] * (len(self._coefficients) - 1) + [Fraction(Decimal(str(other)))]

        return self + Angle(other_angle)

    def __sub__(self, other):
        """
        INTENT:
        Performs subtraction:
          Angle - Angle
          Angle - numbers.Real

        PRE1: other is instance of Angle or numbers.Real
        PRE2: if other is Angle, then self.get_dimension() == other.get_dimension()
        """

        # PRE1
        if not isinstance(other, Angle) and not isinstance(other, numbers.Real):
            error_msg = 'Angle: Trying to subtract <{}> object from an Angle object. Angle or int or float is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        # PRE2
        if isinstance(other, Angle) and self.get_dimension() != other.get_dimension():
            error_msg = 'Angle: minuend and subtrahend should have the same dimension! {} != {}'
            raise Exception(error_msg.format(self.get_dimension(), other.get_dimension()))

        other_angle = None
        if isinstance(other, numbers.Real):
            other_angle = [Fraction(0)] * (len(self._coefficients) - 1) + [Fraction(Decimal(str(-other)))]
        elif isinstance(other, Angle):
            other_angle = list(map(lambda x: -x, other._coefficients))

        return self + Angle(other_angle)

    def __rsub__(self, other):
        """
        INTENT:
        Performs subtraction:
          numbers.Real - Angle

        PRE1: other is instance of numbers.Real
        PRE2: if other is Angle, then self.get_dimension() == other.get_dimension()
        """

        # PRE1
        if not isinstance(other, numbers.Real):
            error_msg = 'Angle: Trying to subtract Angle object from a <{}> object. int or float is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        other_angle = list(map(lambda x: -x, self._coefficients))
        return Angle(other_angle) + other

    def __truediv__(self, other):
        """
        INTENT:
        Performs division:
          Angle / numbers.Real

        PRE1: other is instance of numbers.Real
        """

        # PRE1
        if not isinstance(other, numbers.Real):
            error_msg = 'Angle: Trying to divide an Angle object by a <{}> object. int or float is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        other_angle = list(map(lambda x: x / Fraction(Decimal(str(other))), self._coefficients))
        return Angle(other_angle)

    def __mul__(self, other):
        """
        INTENT:
        Performs multiplication:
          Angle * numbers.Real

        PRE1: other is instance of numbers.Real
        """

        # PRE1
        if not isinstance(other, numbers.Real):
            error_msg = 'Angle: Trying to multiply an Angle object to a <{}> object. int or float is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        other_angle = list(map(lambda x: x * Fraction(Decimal(str(other))), self._coefficients))
        return Angle(other_angle)

    def __rmul__(self, other):
        """
        INTENT:
        Performs multiplication:
          numbers.Real * Angle

        PRE1: other is instance of numbers.Real
        """

        # PRE1
        if not isinstance(other, numbers.Real):
            error_msg = 'Angle: Trying to multiply an Angle object to a <{}> object. int or float is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        return self * other

    def __eq__(self, other):
        """
        Performs comparison of:
            - two angle objects (Angle == Angle)
            - an angle object and a constant value of int (Angle == int or int == Angle)

        PRE1
        Other is an instance of Angle or int

        PRE2
        If other is Angle, dimensions of other and self are equal
        """

        # PRE1
        if not isinstance(other, Angle) and not isinstance(other, int):
            error_msg = 'Angle: Trying to compare {} object to Angle object. Angle or int is required.'
            raise TypeError(error_msg.format(type(other).__name__))

        # PRE2
        if isinstance(other, Angle) and len(self._coefficients) != len(other._coefficients):
            error_msg = 'Angle: Trying to compare two Angle objects of different dimension.'
            raise Exception(error_msg)

        if isinstance(other, int):
            a = Angle([Fraction(0)] * (self.get_dimension() - 1) + [Fraction(other)])
            return self == a

        for i in range(len(self._coefficients)):
            if self._coefficients[i] != other._coefficients[i]:
                return False

        return True

    def __ne__(self, other):
        """
        Performs comparison of:
            - two angle objects (Angle != Angle)
            - an angle object and a constant value of int (Angle != int or int != Angle)

        PRE1
        Other is an instance of Angle or int.

        PRE2
        If other is Angle, dimensions of other and self are equal.

        NOTE
        Implementation of PRE1 and PRE2 are delegated to self.__eq__()
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

        # prepares first n-1 _coefficients
        result = ''
        for i in range(len(self._coefficients) - 1):
            a = self._coefficients[i]
            if a > 0:
                result += (' + ' + str(a) if a != 1 else ' + ') + GREEK_LETTERS[i]
            elif a < 0:
                result += (' - ' + str(abs(a)) if abs(a) != 1 else ' - ') + GREEK_LETTERS[i]

        # prepares the last coefficient
        a = self._coefficients[-1]
        if a > 0:
            result += ' + ' + str(a)
        elif a < 0:
            result += ' - ' + str(abs(a))

        # restoring the sign before the first coefficient
        if result[1] == '-':
            result = '-' + result[3:]
        elif result[1] == '+':
            result = result[3:]

        return result

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        """
        INTENT
        User defined objects in Python are mutable by default. Overriding this method enables to make them immutable.
        This method is specifically written to be able to:
        1. compare two sets of Angle objects with each other.
        2. using collections.Counter for comparing two lists of Angle objects
        Both Python sets and collections.Counter require objects to be hashable.
        """

        # relies on _coefficients
        result = ''
        for c in self._coefficients:
            result += str(c)
        return hash(result)

    def get_coefficients(self):
        return self._coefficients

    def get_dimension(self):
        return len(self._coefficients)

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

        return bool(self.get_coefficients())

    @classmethod
    def from_str(cls, a_str, a_dimension):
        """
        INTENT
        This is a special class method which allows to instantiate an Angle object
        of dimension a_dimension from a string value a_str.

        PRE1
        a_dimension < len(GREEK_LETTERS)

        PRE2
        a_dimension == len(a_str.split())

        PRE3
        a_str is in one of the forms:
            - 'x' for unknown
            - 'a b ... z' for aα + bβ + ... + z
                where a, b, ..., z are either of these:
                    - positive/negative integers (g.e. 1, 2, -90, -9, etc)
                    - positive/negative fractions (g.e. 1/2, 3/5, -6/19, -9/2, etc)

        USAGE
        a = Angle.from_str('x', 4)
        print(a.get_coefficients())  # [0, 0, 0, 0]

        b = Angle.from_str('1 0 90', 3)
        print(b)  # α + 90

        c = Angle.from_str('r 1 90', 3)  # ERROR! r is a letter

        d = Angle.from_str('1/3 1/3 -1/3 90')
        print(d.get_coefficients())  # [1/3α + 1/3β - 1/3γ + 90]
        """

        if a_str == 'x':
            a = Angle([])
            return a

        # we assume that _coefficients are separated by space
        coefs = a_str.split()
        fraction_coefs = list()
        for coef in coefs:
            fraction_coefs.append(Fraction(coef))

        return Angle(fraction_coefs)
