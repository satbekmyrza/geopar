import unittest
from anglenew import Angle

__author__ = 'satbek'


class TestAngle(unittest.TestCase):

    def setUp(self):
        self.angle1 = Angle([1, 2, 3, 4, 5, 60])
        self.angle2 = Angle([2, 3, 4, 5, 6, 70])
        self.angle3 = Angle([2, 4, 6, 8, 100])

    def test_add(self):
        # Angle + Angle
        self.assertEqual(self.angle1 + self.angle2, Angle([3, 5, 7, 9, 11, 130]))

        # Angle + int
        self.assertEqual(self.angle1 + 10, Angle([1, 2, 3, 4, 5, 70]))
        self.assertEqual(self.angle1 + (-10), Angle([1, 2, 3, 4, 5, 50]))

    def test_radd(self):
        # int + Angle
        self.assertEqual(15 + self.angle2, Angle([2, 3, 4, 5, 6, 85]))

    def test_sub(self):
        # Angle - Angle
        self.assertEqual(self.angle2 - self.angle1, Angle([1, 1, 1, 1, 1, 10]))
        self.assertEqual(self.angle1 - self.angle2, Angle([-1, -1, -1, -1, -1, -10]))

        # Angle - int
        self.assertEqual(self.angle1 - 25, Angle([1, 2, 3, 4, 5, 35]))

    def test_rsub(self):
        # int - Angle
        self.assertEqual(200 - self.angle1, Angle([-1, -2, -3, -4, -5, 140]))

    def test_floordiv(self):
        # Angle // int
        self.assertEqual(self.angle3 // 2, Angle([1, 2, 3, 4, 50]))

    def test_mul(self):
        # Angle * int
        self.assertEqual(self.angle3 * 2, Angle([4, 8, 12, 16, 200]))

    def test_rmul(self):
        # int * Angle
        self.assertEqual(2 * self.angle3, Angle([4, 8, 12, 16, 200]))