import unittest
from Geopar.angle import Angle

__author__ = 'satbek'


class TestAngle(unittest.TestCase):

    def setUp(self):
        self.angle0 = Angle([1, 1, 90])
        self.angle1 = Angle([1, 1, -90])
        self.angle2 = Angle([1, -1, 90])
        self.angle3 = Angle([1, -1, -90])
        self.angle4 = Angle([-1, 1, 90])
        self.angle5 = Angle([-1, 1, -90])
        self.angle6 = Angle([-1, -1, 90])
        self.angle7 = Angle([-1, -1, -90])

        # print(self.angle0)
        # print(self.angle1)
        # print(self.angle2)
        # print(self.angle3)
        # print(self.angle4)
        # print(self.angle5)
        # print(self.angle6)
        # print(self.angle7)

        self.anglee0 = Angle([1, 1, 90])
        self.anglee1 = Angle([0, 1, 90])
        self.anglee2 = Angle([1, 0, 90])
        self.anglee3 = Angle([1, 1, 0])
        self.anglee4 = Angle([0, 0, 90])
        self.anglee5 = Angle([0, 1, 0])
        self.anglee6 = Angle([1, 0, 0])
        self.anglee7 = Angle([0, 0, 0])

        print(self.anglee0)
        print(self.anglee1)
        print(self.anglee2)
        print(self.anglee3)
        print(self.anglee4)
        print(self.anglee5)
        print(self.anglee6)
        print(self.anglee7)

    def test_add(self):
        self.assertTrue(self.angle0 + self.angle1 == Angle([2, 2, 0]))
        self.assertTrue(self.angle1 + self.angle2 == Angle([2, 0, 0]))

    def test_equality(self):
        self.assertTrue(self.angle0 != self.angle1)
        self.assertTrue(self.angle2 != self.angle3)

    def test_is_known(self):
        self.assertTrue(self.angle1.is_known())

    def test_from_str(self):
        pass