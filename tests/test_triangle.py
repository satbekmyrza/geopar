import unittest
from geopar.triangle import Triangle
from geopar.angle import Angle
from fractions import Fraction

__author__ = 'satbek'


class TestTriangle(unittest.TestCase):

    def setUp(self):
        self.triangle0 = Triangle([1, 2, 3], [20, 30, 130])
        print(self.triangle0)
        self.triangle1 = Triangle([2, 1, 77], [130, 20, 30])
        print(self.triangle1)
        self.triangle2 = Triangle([1, 77, 88], [Angle([30,40,110]), Angle.from_str('x', 3), Angle([60,60,60])])
        print(self.triangle2)

        self.aa = Angle.from_str('1/3 1/3 1/3 60', 4)
        self.ab = Angle.from_str('-1/3 1/3 -1/3 45', 4)
        self.ac = Angle.from_str('x', 4)
        self.triangle3 = Triangle([1, 2, 3], [self.aa,self.ab,self.ac])

        self.aaa = Angle.from_str('1/3 1/3 1/3 60', 4)
        self.aba = Angle.from_str('-1/3 1/3 -1/3 45', 4)
        self.aca = Angle.from_str('x', 4)
        self.triangle3a = Triangle([1, 2, 3], [self.aaa, self.aba, self.aca])

    def test_hash(self):
        self.assertEqual(hash(self.triangle0), hash(self.triangle0))  # a == a
        self.assertEqual(hash(self.triangle1), hash(self.triangle1))  # b == b
        self.assertNotEqual(hash(self.triangle0), hash(self.triangle1))  # a != b

        self.assertEqual(hash(self.triangle3), hash(self.triangle3))  # c == c
        self.assertEqual(hash(self.triangle3), hash(self.triangle3a))  # c == d

    def test_get_angles(self):
        self.assertTrue(20 in self.triangle0.get_angles())
        self.assertTrue(30 in self.triangle1.get_angles())
        self.assertTrue(Angle.from_str('30 40 110', 3) in self.triangle2.get_angles())

    def test_angle_of_point(self):
        self.assertTrue(20 == self.triangle0.angle_of_point(1))
        self.assertTrue(30 == self.triangle1.angle_of_point(77))
        self.assertTrue(Angle([60,60,60]) == self.triangle2.angle_of_point(88))

    def test_has_point(self):
        self.assertTrue(self.triangle0.has_point(1))
        self.assertTrue(self.triangle0.has_point(3))
        self.assertFalse(self.triangle0.has_point(4))
        self.assertTrue(self.triangle1.has_point(77))

    def test_preceding_and_next_point(self):
        self.assertEqual(3, self.triangle0.point_following(2))
        self.assertEqual(1, self.triangle0.point_following(3))
        self.assertEqual(1, self.triangle1.point_preceding(77))

    def test_find_third_angle(self):
        self.assertTrue(self.triangle2.complete_unknown_angle())

    def test_complete_unknown_angle(self):
        self.triangle3.complete_unknown_angle()
        print(self.triangle3)