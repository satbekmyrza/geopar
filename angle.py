__author__ = 'satbek'


class Angle:
    """
    INTENT:
    Defines an angle in terms of THREE integer numbers.
    Let's say the angle is: aα + bβ + c
    Then it is sufficient to have [a, b, c] to express that angle.
    Thus, we have self.coefficients list to store those values.
    This class enables you to work with variable angles.

    IMPORTANT:
    If all of the self.coefficients are 0, then the angle is said to be unknown.

    CLASS INVARIANT:
    if all of self.coefficients are 0, then the angle is said to be unknown.

    NOTES:
    1. This class supports is 3-dimensional Angle objects.
       N-dimensionality can be implemented in future versions.
    2. Works with only int coefficients.
       float coefficient support can be implemented.

    ISSUES:
    1. __str__ method does not work with negative coefficients in a proper way. [SOLVED]

    """

    def __init__(self, coefficients):
        """
        PRE:
        coefficients is a list of 3 integer numbers positive or negative.

        POST:
        an angle with these coefficients is defined.
        """

        self.coefficients = coefficients

    def __add__(self, other):
        # INTENT:
        # Defines addition of two angles: self and other.

        # PRE:
        # other is an Angle object OR int object

        # POST:
        # summation is performed.

        # RAISES:
        # TypeError, if other is not an Angle object OR int object.

        # NOTES:
        # write unittest for this method

        if not (isinstance(other, Angle) or isinstance(other, int)):
            raise TypeError('Trying to add non-Angle or non-int object to an Angle object.')

        result = None

        if isinstance(other, int):
            result = [self.coefficients[0], self.coefficients[1],
                      self.coefficients[2] + other]

        elif isinstance(other, Angle):
            result = [self.coefficients[0] + other.coefficients[0],
                      self.coefficients[1] + other.coefficients[1],
                      self.coefficients[2] + other.coefficients[2]]

        return Angle(result)

    def __radd__(self, other):
        # INTENT:
        # Is invoked when Angle object is to the right of '+' sign. For example:
        # a = Angle(0, 0, 45)
        # b = 45 + a
        # This method is specifically written to allow
        # built-in sum() function to work properly with Angle objects.

        # PRE:
        # other is an instance of int

        # POST:
        # summation is performed

        # RAISES:
        # TypeError, if other is not an instance of int

        # NOTES:
        # unittest should be implemented

        if not isinstance(other, int):
            raise Exception('Trying to add Angle object to a non-int object.')

        return self + Angle([0, 0, other])

    def __sub__(self, other):
        # INTENT:
        # Defines subtraction of two angles: self and other.
        # {Angle - Angle} OR {Angle - int}

        # PRE:
        # other is an Angle object OR an int object

        # POST:
        # subtraction is performed

        # RAISES:
        # TypeError, if other is not an Angle object OR int object.

        # NOTES
        # unittest should be implemented

        if not (isinstance(other, Angle) or isinstance(other, int)):
            raise TypeError('Trying to subtract non-Angle or non-int object from an Angle object.')

        result = None

        if isinstance(other, int):
            result = [self.coefficients[0], self.coefficients[1],
                      self.coefficients[2] - other]

        elif isinstance(other, Angle):
            result = [self.coefficients[0] - other.coefficients[0],
                      self.coefficients[1] - other.coefficients[1],
                      self.coefficients[2] - other.coefficients[2]]

        return Angle(result)

    def __rsub__(self, other):
        # INTENT
        # Is invoked when Angle object is to the right of '-' sign. For example:
        # a = Angle(0, 0, 45)
        # b = 90 - a

        # PRE
        # other is an instance of int

        # POST
        # subtraction is performed

        # RAISES
        # TypeError, if other is not an instance of int

        # NOTES
        # unittest should be implemented

        if not isinstance(other, int):
            raise TypeError('Trying to subtract Angle object from a non-int object.')

        return Angle([0, 0, other]) - self

    def __floordiv__(self, other):
        # INTENT
        # Makes an Angle object divisible by integer value.
        # For example, if you need an angle which is three times smaller than, say, _a_,
        # you write _b_ = _a_ // 3

        # PRE
        # other is an instance of int

        # POST
        # floor division is performed

        # RAISES
        # TypeError, if other is not an instance of int

        # NOTES
        # unittest should be implemented

        if not isinstance(other, int):
            raise TypeError('Trying to floor-div an Angle object by a non-int value.')

        return Angle([self.coefficients[0]//other, self.coefficients[1]//other, self.coefficients[2]//other])

    def __mul__(self, other):
        # INTENT
        # makes an Angle object multipliable to an int value

        # PRE
        # other is an instance of int

        # POST
        # multiplication is performed

        # RAISES
        # TypeError, if other is not an instance of int

        # NOTES
        # unittest should be performed

        if not isinstance(other, int):
            raise TypeError('Trying to multiply an Angle object to a non-int value.')

        return Angle([self.coefficients[0] * other, self.coefficients[1] * other, self.coefficients[2] * other])

    def __rmul__(self, other):
        # INTENT
        # makes an Angle object multipliable by an int value,
        # when the Angle object is on the right side of '*' sign

        # PRE
        # other is an instance of int

        # POST
        # multiplication is performed

        # RAISES
        # TypeError, when other is not an instance of int

        # NOTES
        # unittest should be implemented

        if not isinstance(other, int):
            raise TypeError('Trying to multiply an Angle object to a non-int value.')

        return Angle([self.coefficients[0] * other, self.coefficients[1] * other, self.coefficients[2] * other])

    def __eq__(self, other):
        # INTENT
        # tests Angle objects for equality

        # PRE
        # other is an Angle object

        # POST
        # True if equal; False, otherwise

        # RAISES
        # TypeError, if other is not an Angle object

        # NOTES
        # unittest should be implemented

        if self.coefficients[0] == other.coefficients[0]:
            if self.coefficients[1] == other.coefficients[1]:
                if self.coefficients[2] == other.coefficients[2]:
                    return True
        return False

    def __ne__(self, other):
        # INTENT
        # tests Angle objects for non-equality

        # PRE
        # other is an Angle object

        # POST
        # True if equal; False, otherwise

        # RAISES
        # TypeError, if other is not an Angle object

        # NOTES
        # unittest should be implemented

        return not self.__eq__(other)

    def __str__(self):
        # INTENT
        # returns a string representation of self for printing it directly from print()

        # POST
        # string representation of self is returned

        # NOTES
        # 2α + 2β + 2
        # 2α + 2β - 2
        # 2α - 2β + 2
        # 2α - 2β - 2
        # -2α + 2β + 2
        # -2α + 2β - 2
        # -2α - 2β + 2
        # -2α - 2β - 2

        result = ""
        if self.coefficients[0] != 0:

            # checking if equals to 1
            if self.coefficients[0] == -1:
                result += "-α"
            elif self.coefficients[0] == 1:
                result += "α"
            else:
                result += str(self.coefficients[0]) + "α"

            if self.coefficients[1] != 0:
                if self.coefficients[1] > 0:
                    result += " + "
                else:
                    result += " - "

                # checking if equals to 1
                if abs(self.coefficients[1]) == 1:
                    result += "β"
                else:
                    result += str(abs(self.coefficients[1]))
                    result += "β"

                if self.coefficients[2] != 0:
                    if self.coefficients[2] > 0:
                        result += " + "
                    else:
                        result += " - "
                    result += str(abs(self.coefficients[2]))
            else:
                if self.coefficients[2] != 0:
                    if self.coefficients[2] > 0:
                        result += " + "
                    else:
                        result += " - "
                    result += str(abs(self.coefficients[2]))
        else:
            if self.coefficients[1] != 0:

                # checking if equals to 1
                if abs(self.coefficients[1]) == 1:
                    result += "β"
                else:
                    result += str(abs(self.coefficients[1]))
                    result += "β"

                if self.coefficients[2] != 0:
                    if self.coefficients[2] > 0:
                        result += " + "
                    else:
                        result += " - "
                    result += str(abs(self.coefficients[2]))
            else:
                if self.coefficients[2] != 0:
                    result += str(self.coefficients[2])
                else:
                    result += "x"
        return result

    def __hash__(self):
        # INTENT
        # User defined objects in Python are mutable by default.
        # Overriding this method enables to make them immutable.
        # This method is specifically written to be able to compare two sets of Angle objects with each other.
        # Python sets require their elements to be hashable.
        # upd.: using collections.Counter for comparing two lists of Angle objects

        # POST
        # hash of self is returned

        # NOTES

        # relying on self.coefficients to calculate hash
        temp = str(self.coefficients[0]) + str(self.coefficients[1]) + str(self.coefficients[2])
        return hash(temp)

    def get_coefficients(self):
        # POST
        # self.coefficients is returned.

        return self.coefficients

    def is_known(self):
        # INTENT
        # enables the user to know whether the value of self is known

        # POST
        # True, if self is known; False, otherwise

        return not (self.coefficients[0] == 0 and self.coefficients[1] == 0 and self.coefficients[2] == 0)

    @classmethod
    def from_str(cls, a_str):
        # INTENT
        # This is a special class method, which allows to instantiate an Angle object from a string value.

        # USAGE
        # a = Angle.from_str('x')
        # print(a.get_coefficients())  # [0, 0, 0]
        # b = Angle.from_str('1,0,90')
        # print(b)  # α + 90
        # c = Angle.from_str('a, 1, 90')  # ERROR!

        # PRE
        # a_str should be in the form:
        #     'x' for unknown OR
        #     'a, b, c'--where a, b and c are integer numbers--for aα + bβ + c

        # POST
        # a newly created Angle object is returned

        # RAISES
        # nums = list(map(int, a_str.split(','))) will raise an error if a_str contains alphabetic characters OR
        # doesn't have three comma separated numbers.

        # NOTES
        # work on detailed exception

        if a_str == 'x':
            return Angle([0, 0, 0])
        nums = list(map(int, a_str.split()))
        return Angle(nums)
