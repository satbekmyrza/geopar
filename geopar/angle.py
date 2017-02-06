from fractions import Fraction
from decimal import Decimal
from geopar.extras import to_fraction
from operator import add

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

    def __init__(self, some_coefficients):
        """
        PRE1: len(some_coefficients) <= 16
        PRE2: isinstance(coef, (Fraction, int, float)) is True for every coef in self._coefficients
        """

        # (Converted): self._coefficients[i] is the Fraction equivalent of some_coefficients[i]
        # for all i, such that 0 <= i < len(some_coefficients)
        self._coefficients = []
        for i in range(len(some_coefficients)):
            coef = some_coefficients[i]
            if isinstance(coef, (int, float)):
                self._coefficients.append(to_fraction(coef))
            elif isinstance(coef, Fraction):
                self._coefficients.append(coef)

    def __add__(self, an_angle):
        """
        ----------------------------------------------------------------------------------------------------------------
        Intent: Implementation of "+" arithmetic operation.
                This method is invoked when there is something to be added to self.
        ----------------------------------------------------------------------------------------------------------------
        Usage:
        Angle + Angle
        Angle + int
        Angle + float
        ----------------------------------------------------------------------------------------------------------------
        Pre1 (Known): self.is_known()

        Pre2 (Correct parameter): EITHER is_instance(an_angle, (int, float)) OR
                                  ( is_instance(an_angle, Angle) AND
                                    an_angle.is_known() AND
                                    an_angle.get_dimension() = self.get_dimension() )
        ----------------------------------------------------------------------------------------------------------------
        Post1 (Coefficients obtained): an_angle_coefs is a list of length self.get_dimension() whose elements are
                                       EITHER an_angle.get_coefficients() when is_instance(an_angle, Angle)
                                       OR [0, 0, ..., an_angle] when is_instance(an_angle, (int, float))

        Post2 (Coefficients added): return_angle_coefs is a list of length self.get_dimension() where
                                    return_angle_coefs[i] = self._coefficients[i] + an_angle_coefs[i]

        Post3 (Sum returned): Angle with coefficients return_angle_coefs is returned
        ----------------------------------------------------------------------------------------------------------------
        """

        # === (Coefficients Obtained)
        an_angle_coefs = []
        if isinstance(an_angle, Angle):
            an_angle_coefs = an_angle.get_coefficients()
        elif isinstance(an_angle, (int, float)):
            an_angle_coefs = [Fraction(0)] * (self.get_dimension() - 1) + [to_fraction(an_angle)]

        # === (Coefficients added)
        return_angle_coefs = list(map(add, self._coefficients, an_angle_coefs))

        # === (Sum returned)
        return Angle(return_angle_coefs)

    def __radd__(self, an_angle):
        """
        Intent: Implementation of "+" arithmetic operation.
                This method is invoked when self is to be added to something.

        Usage:
        int + Angle
        float + Angle
        """

        # delegated to self.__add__
        return self + an_angle

    def __sub__(self, an_angle):
        """
        Intent: Implementation of "-" arithmetic operation.
                This method is invoked when there is something to be subtracted from self.

        Usage:
        Angle - Angle
        Angle - int
        Angle - float

        PRE1: self.is_known()
        PRE2: is_instance(an_angle, (Angle, int, float))
        PRE3: EITHER !is_instance(an_angle, Angle) OR
              an_angle.is_known() AND self.get_dimension() = an_angle.get_dimension()
        """

        # (Converted and Negated): negated_angle is an Angle instance, where
        # negated_angle = -an_angle AND
        # negated_angle.get_dimension() = self.get_dimension() AND
        # negated_angle.get_coefficients()[i] is Fraction instance for all i, such that
        # 0 <= i < temp_angle.get_dimension()
        negated_coefs = None
        if isinstance(an_angle, (int, float)):
            negated_coefs = [to_fraction(0)] * (len(self._coefficients) - 1) + [to_fraction(-an_angle)]
        elif isinstance(an_angle, Angle):
            negated_coefs = list(map(lambda x: -x, an_angle.get_coefficients()))
        negated_angle = Angle(negated_coefs)

        # (Subtracted): self - an_angle is returned
        return self + negated_angle

    def __rsub__(self, an_angle):
        """
        Intent: Implementation of "-" arithmetic operation.
                This method is invoked when self is to be subtracted from something.

        Usage:
        int - Angle
        float - Angle
        """

        # an_angle - self = negated_self + an_angle
        negated_self = Angle(list(map(lambda x: -x, self._coefficients)))

        # delegated to self.__add__
        return negated_self + an_angle

    def __truediv__(self, a_number):
        """
        Intent: Implementation of "/" arithmetic operation.
                This method is invoked when self is to be divided by a real number.

        Usage:
        Angle / int
        Angle / float

        PRE1: self.is_known()
        PRE2: is_instance(a_number, (int, float))
        """

        # (Divided): (self / a_number) is returned
        result_coefficients = list(map(lambda x: x / to_fraction(a_number), self._coefficients))
        return Angle(result_coefficients)

    def __mul__(self, a_number):
        """
        Intent: Implementation of "*" arithmetic operation.
                This method is invoked when self is to be multiplied by a real number.

        Usage:
        Angle * int
        Angle * float

        PRE1: self.is_known()
        PRE2: is_instance(a_number, (int, float))
        """

        # (Multiplied): (self * a_number) is returned
        results_coefficients = list(map(lambda x: x * to_fraction(a_number), self._coefficients))
        return Angle(results_coefficients)

    def __rmul__(self, a_number):
        """
        Intent: Implementation of "*" arithmetic operation.
                This method is invoked when a real number is to be multiplied by self.

        Usage:
        int * Angle
        float * Angle
        """

        # delegated to self.__mul__
        return self * a_number

    def __eq__(self, an_angle):
        """
        Intent: Implementation of "==" test for equality operation.
                This method is invoked when self is to be checked for equality with something.

        Usage:
        Angle == Angle
        Angle == int
        Angle == float
          int == Angle
        float == Angle

        PRE1: self.is_known()
        PRE2: is_instance(an_angle, (Angle, int, float))
        PRE3: EITHER !is_instance(an_angle, Angle) OR
              an_angle.is_known() AND self.get_dimension() = an_angle.get_dimension()
        """

        # (Converted): an_angle is an Angle instance, where
        # an_angle.get_dimension() = self.get_dimension() AND
        # an_angle.get_coefficients()[i] is Fraction instance for all i,
        # such that 0 <= i < an_angle.get_dimension()
        if isinstance(an_angle, (int, float)):
            an_angle = Angle([to_fraction(0)] * (self.get_dimension() - 1) + [to_fraction(an_angle)])

        # (Compared): self._coefficients[i] is compared to an_angle.get_coefficients()[i] for all i,
        # such that 0 <= i < len(self._coefficients)
        an_angle_coefs = an_angle.get_coefficients()
        for i in range(len(self._coefficients)):
            if self._coefficients[i] != an_angle_coefs[i]:
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
