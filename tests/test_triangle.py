import unittest
from triangle import Triangle
from angle import Angle

__author__ = 'satbek'


class TestTriangle(unittest.TestCase):

    def setUp(self):
        self.triangle0 = Triangle([1, 2, 3], [20, 30, 130])
        print(self.triangle0)
        self.triangle1 = Triangle([2, 1, 77], [130, 20, 30])
        print(self.triangle1)
        self.triangle2 = Triangle([1, 77, 88], [Angle([30,40,110]), Angle.from_str('x', 3), Angle([60,60,60])])
        print(self.triangle2)

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