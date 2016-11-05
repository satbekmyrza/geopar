import unittest
from geopar.angle import Angle
from fractions import Fraction

__author__ = 'satbek'


class TestAngle(unittest.TestCase):

    def setUp(self):
        self.angle1 = Angle([1, 2, 3, 4, 5, 60])
        self.angle2 = Angle([2, 3, 4, 5, 6, 70])
        self.angle12 = Angle([3, 5, 7, 9, 11, 130])
        self.angle3 = Angle([2, 4, 6, 8, 100])

    def test_add(self):
        # Angle + Angle
        # print('({}) + ({}) = {}'.format(self.angle1, self.angle2, self.angle12))
        self.assertEqual(self.angle1 + self.angle2, self.angle12)
        # Angle + numbers.Real
        self.assertEqual(self.angle1 + 10, Angle([1, 2, 3, 4, 5, 70]))
        self.assertEqual(self.angle1 + (-100.0), Angle([1, 2, 3, 4, 5, -40]))

        # print(self.angle1 + 12.1212)

    def test_radd(self):
        # numbers.Real + Angle
        self.assertEqual(15 + self.angle2, Angle([2, 3, 4, 5, 6, 85]))
        self.assertEqual(15.0 + self.angle2, Angle([2, 3, 4, 5, 6, 85]))

    def test_sub(self):
        # Angle - Angle
        self.assertEqual(self.angle2 - self.angle1, Angle([1, 1, 1, 1, 1, 10]))
        self.assertEqual(self.angle1 - self.angle2, Angle([-1, -1, -1, -1, -1, -10]))

        # Angle - numbers.Real
        self.assertEqual(self.angle1 - 25, Angle([1, 2, 3, 4, 5, 35]))
        self.assertEqual(self.angle1 - 50.0, Angle([1, 2, 3, 4, 5, 10]))

    def test_rsub(self):
        # numbers.Real - Angle
        self.assertEqual(200 - self.angle1, Angle([-1, -2, -3, -4, -5, 140]))
        self.assertEqual(200.5 - self.angle1, Angle([-1, -2, -3, -4, -5, 140.5]))

    def test_truediv(self):
        # Angle / numbers.Real
        self.assertEqual(self.angle3 / 2, Angle([1, 2, 3, 4, 50]))
        self.assertEqual(self.angle1 / 2, Angle.from_str('.5 1 1.5 2 2.5 30', 6))

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

