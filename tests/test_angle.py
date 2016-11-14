import unittest
from geopar.angle import Angle
from geopar.angle import GREEK_LETTERS
from fractions import Fraction

__author__ = 'satbek'


class TestAngle(unittest.TestCase):
    def setUp(self):
        self.a_constant = Angle([90])
        self.a_constant_neg = Angle([-90])

        self.a_two1 = Angle([1, 45])
        self.a_two2 = Angle([0, 45])
        self.a_two3 = Angle([2, -45])
        self.a_two4 = Angle([0, -45])

        self.angle1 = Angle([1, 2, 3, 4, 5, 60])
        self.angle2 = Angle([2, 3, 4, 5, 6, 70])
        self.angle12 = Angle([3, 5, 7, 9, 11, 130])
        self.angle3 = Angle([2, 4, 6, 8, 100])
        self.angle4 = Angle([2, 4, 6, 8, 100])
        self.angle5 = Angle([0, 0, 0, 0, 0, 90])

    def test_init(self):
        # PRE 1
        # len(coefficients) > 16
        with self.assertRaises(Exception):
            angle = Angle([1] * (len(GREEK_LETTERS) + 2))

        # PRE 2
        # wrong type
        with self.assertRaises(Exception):
            angle = Angle(['str value'])

        # Force conversion of int, float coefficients to Fraction
        angle = Angle([1, 2, Fraction(3), 4.0, Fraction(1, 3)])
        for coef in angle.get_coefficients():
            self.assertTrue(isinstance(coef, Fraction))

    def test_add(self):
        a = Angle([])
        b = Angle([1, 90])
        c = Angle([1, 1, 90])

        # PRE1
        # self is unknown
        with self.assertRaises(Exception):
            d = a + b

        # PRE2
        # other is not Angle|int|float
        with self.assertRaises(Exception):
            d = b + 'str'

        # PRE3
        # other is unknown
        with self.assertRaises(Exception):
            d = b + a
        # self.get_dimension != other.get_dimension
        with self.assertRaises(Exception):
            d = b + c

        # Angle + Angle
        self.assertEqual(Angle([10]) + Angle([20]), Angle([30]))
        self.assertEqual(Angle([1, 10]) + Angle([0, -20]), Angle([1, -10]))
        # Angle + int
        self.assertEqual(Angle([1, 10]) + 90, Angle([1, 100]))
        self.assertEqual(Angle([1, 2, 3, 4, -10]) + 90, Angle([1, 2, 3, 4, 80]))
        # Angle + float
        self.assertEqual(Angle([1, 10]) + 1.5, Angle([1, 11.5]))
        self.assertEqual(Angle([-1, 0, -10]) + 1.5, Angle([-1, 0, -8.5]))

    def test_radd(self):
        # exceptions are delegated to self.__add__()
        a = Angle([])
        b = Angle([1, 90])

        # PRE1
        # self is unknown
        with self.assertRaises(Exception):
            d = 90 + a

        # PRE2
        # other is not Angle|int|float
        with self.assertRaises(Exception):
            d = 'str' + b

        # int + Angle
        self.assertEqual(90 + Angle([1, 10]), Angle([1, 100]))
        self.assertEqual(90 + Angle([1, 2, 3, 4, -10]), Angle([1, 2, 3, 4, 80]))
        # float + Angle
        self.assertEqual(1.5 + Angle([1, 10]), Angle([1, 11.5]))
        self.assertEqual(1.5 + Angle([-1, 0, -10]), Angle([-1, 0, -8.5]))

    def test_sub(self):
        a = Angle([])
        b = Angle([1, 90])
        c = Angle([1, 1, 90])

        # PRE1
        # self is unknown
        with self.assertRaises(Exception):
            d = a - b

        # PRE2
        # other is not Angle|int|float
        with self.assertRaises(Exception):
            d = b - 'str'

        # PRE3
        # other is unknown
        with self.assertRaises(Exception):
            d = b - a
        # self.get_dimension != other.get_dimension
        with self.assertRaises(Exception):
            d = b - c

        # Angle - Angle
        self.assertEqual(Angle([10]) - Angle([20]), Angle([-10]))
        self.assertEqual(Angle([1, 10]) - Angle([-3, -20]), Angle([4, 30]))
        # Angle - int
        self.assertEqual(Angle([1, 10]) - 90, Angle([1, -80]))
        self.assertEqual(Angle([1, 2, 3, 4, -10]) - 90, Angle([1, 2, 3, 4, -100]))
        # Angle - float
        self.assertEqual(Angle([1, 10]) - 1.5, Angle([1, 8.5]))
        self.assertEqual(Angle([-1, 0, -10]) - 1.5, Angle([-1, 0, -11.5]))

    def test_rsub(self):
        a = Angle([])
        b = Angle([1, 90])
        c = Angle([1, 1, 90])

        # PRE1
        # self is unknown
        with self.assertRaises(Exception):
            d = 90 - a

        # PRE2
        # other is not int|float
        with self.assertRaises(Exception):
            d = 'str' - b

        # int - Angle
        self.assertEqual(90 - Angle([1, 10]), Angle([-1, 80]))
        self.assertEqual(90 - Angle([1, 2, 3, 4, -10]), Angle([-1, -2, -3, -4, 100]))
        # float - Angle
        self.assertEqual(1.5 - Angle([1, 10]), Angle([-1, -8.5]))
        self.assertEqual(1.5 - Angle([-1, 0, -10]), Angle([1, 0, 11.5]))

    def test_truediv(self):
        a = Angle([])
        b = Angle([1, 2, 3, 30])

        # PRE1
        # self is unknown
        with self.assertRaises(Exception):
            c = a / 2

        # PRE2
        # other is not int|float
        with self.assertRaises(Exception):
            c = a / 'str'

        # Angle / int
        self.assertEqual(b / 2, Angle([.5, 1, 1.5, 15]))
        self.assertEqual(b / 1, b)
        # Angle / float
        self.assertEqual(b / .5, Angle([2, 4, 6, 60]))
        self.assertEqual(b / 2.0, Angle([.5, 1, 1.5, 15]))
        self.assertEqual(b / 1.0, b)

    def test_mul(self):
        # Angle * numbers.Real
        self.assertEqual(self.angle3 * 2, Angle([4, 8, 12, 16, 200]))
        self.assertEqual(self.angle3 * 2.0, Angle([4.0, 8, 12, 16, 200]))

    def test_rmul(self):
        # int * Angle
        self.assertEqual(2 * self.angle3, Angle([4, 8, 12, 16, 200]))

    def test_from_str(self):
        a_str = '-1 2/4 -3/5 4000 -599 6/1'
        dim = 10
        a = Angle.from_str(a_str, dim)

        print(a_str.split())

    def test_eq(self):
        self.assertTrue(self.angle3 == self.angle4)
        self.assertTrue(self.angle1 == self.angle1)
        self.assertTrue(90 == self.angle5)
        self.assertTrue(self.angle5 == 90)

    def test_str(self):
        print(self.a_constant)
        print(self.a_constant_neg)
        print(self.a_two1)
        print(self.a_two2)
        print(self.a_two3)
        print(self.a_two4)
