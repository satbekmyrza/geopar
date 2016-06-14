import unittest
from Geopar.anglenew import Angle

__author__ = 'satbek'


class TestAngle(unittest.TestCase):

    def setUp(self):
        self.angle1 = Angle([1, 2, 3, 4, 5, 60])
        self.angle2 = Angle([2, 3, 4, 5, 6, 70])

    def test_add(self):
        # Angle + Angle
        self.assertEqual(self.angle1 + self.angle2, Angle([3, 5, 7, 9, 11, 130]))

        # Angle + int
        self.assertEqual(self.angle1 + 10, Angle([1, 2, 3, 4, 5, 70]))
        self.assertEqual(self.angle1 + (-10), Angle([1, 2, 3, 4, 5, 50]))
