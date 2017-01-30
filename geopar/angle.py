from fractions import Fraction
from decimal import Decimal

__author__ = 'satbek'

# allows support for up to len(GREEK_LETTERS) variables (currently 15)
GREEK_LETTERS = 'αβγδεηθλπρστμφω'


class Angle:
    """
    Defines a geometric angle in terms of a list of Fractions.

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

    USAGE:
    a = Angle([])
    a.is_known() # False
    print(a) # x

    b = Angle([Fraction(1,2), Fraction(90)])
    print(b) # 1/2α + 90

    c = Angle([1.5, 2, -45]) # int and float values are implicitly converted to Fraction
    print(c) # 3/2α + 2β - 45

    d = Angle([Fraction(1,2), 40.5]) # Fraction, int, float values can be mixed
    print(d) # 1/2α + 81/2


    {{1}} To explain more easily, I used integers as coefficients. However, keep in mind that _coefficients
    contains ONLY objects of built-in Fraction class.
    """

    def __init__(self, coefficients):
        """
        PRE1: len(coefficients) <= 16
        PRE2: isinstance(coef, (Fraction, int, float)) is True for every coef in self._coefficients
        """

        # (Converted): non-Fraction coefficients[i] is implicitly converted to Fraction
        # for all i, such that 0 <= i < len(coefficients)
        for i in range(len(coefficients)):
            coef = coefficients[i]
            if isinstance(coef, (int, float)):
                coefficients[i] = Fraction(Decimal(str(coef)))

        # (Complement): i = len(coefficients)
        self._coefficients = coefficients

    def __add__(self, an_angle):
        """
        Intent: Implementation of "+" arithmetic operation.
                This method is invoked when there is something to be added to self.

        Usage:
        Angle + Angle
        Angle + int
        Angle + float

        PRE1: self.is_known()
        PRE2: is_instance(an_angle, (Angle, int, float))
        PRE3: EITHER !is_instance(an_angle, Angle) OR
              an_angle.is_known() AND self.get_dimension() = an_angle.get_dimension()
        """

        # (Converted): temp_angle is an Angle instance, where
        # temp_angle = an_angle AND
        # temp_angle.get_dimension() = self.get_dimension()
        if isinstance(an_angle, (int, float)):
            temp = [Fraction(0)] * (self.get_dimension() - 1) + [Fraction(Decimal(str(an_angle)))]
            temp_angle = Angle(temp)

        # (Added): self + an_angle is returned
            return self + temp_angle
        return Angle(list(map(sum, zip(self._coefficients, an_angle.get_coefficients()))))

    def __radd__(self, other):
        """
        Implements binary arithmetic operation '+' when other is not an instance of Angle.
        int + Angle
        float + Angle

        Preconditions are delegated to self.__add__()
        """

        return self + other

    def __sub__(self, other):
        """
        Implements binary arithmetic operation '-'.
        Angle - Angle
        Angle - int
        Angle - float

        PRE1: self is known
        PRE2: other is instance of Angle, int, or float
        PRE3: if other is instance Angle, then:
                1. other is known
                2. self.get_dimension() == other.get_dimension()
        """

        # PRE1
        if not self.is_known():
            raise Exception('Self is unknown.')

        # PRE2
        if not isinstance(other, (Angle, int, float)):
            raise Exception('Wrong type provided.')

        # PRE3
        if isinstance(other, Angle):
            if not other.is_known():
                raise Exception('Angle that is subtracted is unknown.')
            if self.get_dimension() != other.get_dimension():
                raise Exception('Angles have different dimensions (subtraction).')

        other_angle_coefficients = None
        if isinstance(other, (int, float)):
            other_angle_coefficients = [Fraction(0)] * (len(self._coefficients) - 1) + [Fraction(Decimal(str(-other)))]
        elif isinstance(other, Angle):
            other_angle_coefficients = list(map(lambda x: -x, other.get_coefficients()))

        return self + Angle(other_angle_coefficients)

    def __rsub__(self, other):
        """
        Implements binary arithmetic operation '-'.
        int - Angle
        float - Angle

        PRE1: other is an instance of int|float
        Remaining preconditions are delegated to self.__add__()
        """

        # PRE1
        if not isinstance(other, (int, float)):
            raise Exception('Wrong type provided.')

        negated_self_coefficients = list(map(lambda x: -x, self._coefficients))
        return Angle(negated_self_coefficients) + other

    def __truediv__(self, other):
        """
        Implements binary arithmetic operation '/'.
        Angle / int
        Angle / float

        PRE1: self is known
        PRE2: other is an instance of int|float
        """

        # PRE1
        if not self.is_known():
            raise Exception('Self is unknown.')

        # PRE2
        if not isinstance(other, (int, float)):
            raise Exception('Wrong type provided.')

        result_coefficients = list(map(lambda x: x / Fraction(Decimal(str(other))), self._coefficients))
        return Angle(result_coefficients)

    def __mul__(self, other):
        """
        Implements binary arithmetic operation '*'.
        Angle * int
        Angle * float

        PRE1: self is known
        PRE1: other is an instance of int|float
        """

        # PRE1
        if not self.is_known():
            raise Exception('Self is unknown.')

        # PRE2
        if not isinstance(other, (int, float)):
            raise Exception('Wrong type provided.')

        results_coefficients = list(map(lambda x: x * Fraction(Decimal(str(other))), self._coefficients))
        return Angle(results_coefficients)

    def __rmul__(self, other):
        """
        Implements binary arithmetic operation '*'.
        int * Angle
        float * Angle

        Preconditions are delegated to self.__mul__()
        """

        return self * other

    def __eq__(self, other):
        """
        Implements binary comparison operation '=='.
        Angle == Angle
        Angle == int
        int == Angle
        Angle == float
        float == Angle

        PRE1: self is known
        PRE2: other is an instance of Angle|int|float
        PRE3: if other is an instance of Angle:
                1. other is known
                2. self.get_dimension() == other.get_dimension()
        """

        # PRE1
        if not self.is_known():
            raise Exception('Self is unknown.')

        # PRE2
        if not isinstance(other, (Angle, int, float)):
            raise Exception('Wrong type provided.')

        # PRE3
        if isinstance(other, Angle):
            if not other.is_known():
                raise Exception('Angle to be compared is unknown.')
            if self.get_dimension() != other.get_dimension():
                raise Exception('Angles to be compared have different dimensions.')

        # other is int, float
        if isinstance(other, (int, float)):
            a = Angle([Fraction(0)] * (self.get_dimension() - 1) + [Fraction(Decimal(str(other)))])
            return self == a

        # other is Angle
        other_coefficients = other.get_coefficients()
        for i in range(len(self._coefficients)):
            if self._coefficients[i] != other_coefficients[i]:
                return False

        return True

    def __ne__(self, other):
        """
        Implements binary comparison operation '!='.
        Angle != Angle
        Angle != int
        int != Angle
        Angle != float
        float != Angle

        Preconditions are delegated to self.__eq__()
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
        User defined objects in Python are mutable by default.
        Overriding __hash__ method enables to make them immutable.
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

    def is_known(self):
        # enables the user to know whether the value of self is known

        return bool(self.get_coefficients())

    @classmethod
    def from_str(cls, a_str):
        """
        INTENT:
        This is a special class method which allows instantiating an Angle object
        of dimension a_dimension from a string value a_str.

        PRE1
        a_str is in one of the forms:
            - 'x' for unknown
            - 'a b ... z' for aα + bβ + ... + z
                where a, b, ..., z are either of these:
                    - positive/negative integers (g.e. 1, 2, -90, -9, etc)
                    - positive/negative float numbers (g.e. 1.2, 2.3, -90.0, -9.0, etc)
                    - positive/negative fractions (g.e. 1/2, 3/5, -6/19, -9/2, etc)

        USAGE
        a = Angle.from_str('x')
        print(a.get_coefficients())  # []

        b = Angle.from_str('1 0 90')
        print(b)  # α + 90

        c = Angle.from_str('r 1 90')  # ERROR! 'r' is a character

        d = Angle.from_str('1/3 1/3 -1/3 90')
        print(d.get_coefficients())  # [1/3, 1/3, -1/3, 90]
        """

        if a_str == 'x':
            return Angle([])

        # we assume that _coefficients are separated by space
        coefficients = a_str.split()
        fraction_coefs = []
        for coef in coefficients:
            if '/' in coef:
                fraction_coefs.append(Fraction(coef))
            else:
                fraction_coefs.append(Fraction(Decimal(coef)))

        return Angle(fraction_coefs)
