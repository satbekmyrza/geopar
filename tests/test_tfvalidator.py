import unittest
from geopar.tfvalidator import TFValidator
from geopar.triangulated_figure import TriangulatedFigure
from geopar.triangle import Triangle
from geopar.extras import EmptyException

__author__ = 'satbek'

# URL1: https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit?usp=sharing


class TestTFValidator(unittest.TestCase):

    def setUp(self):
        self.validator = TFValidator()
        self.tf_empty = TriangulatedFigure()

        # TriangulatedFigure tf1 consists of seven Triangles t1-t7
        # Appearance: URL1 at the top
        self.t1 = Triangle([1, 2, 5], [20, 10, 150])
        self.t2 = Triangle([5, 2, 6], [80, 10, 90])
        self.t3 = Triangle([6, 2, 3], [140, 10, 30])
        self.t4 = Triangle([4, 6, 3], [80, 70, 30])
        self.t5 = Triangle([1, 4, 3], [20, 130, 30])
        self.t6 = Triangle([1, 5, 4], [20, 70, 90])
        self.t7 = Triangle([4, 5, 6], [60, 60, 60])
        self.tf1 = TriangulatedFigure()
        self.tf1.add(self.t1)
        self.tf1.add(self.t2)
        self.tf1.add(self.t3)
        self.tf1.add(self.t4)
        self.tf1.add(self.t5)
        self.tf1.add(self.t6)
        self.tf1.add(self.t7)

    def test_rule_180(self):
        self.assertTrue(self.validator.rule_180(self.tf1))

        with self.assertRaises(EmptyException):
            self.validator.rule_180(self.tf_empty)

    def test_rule_360(self):
        self.assertTrue(self.validator.rule_360(self.tf1))

        with self.assertRaises(Exception):
            self.validator.rule_180(self.tf_empty)

    def test_rule_pairing(self):
        self.assertTrue(self.validator.rule_pairing(self.tf1))

        with self.assertRaises(Exception):
            self.validator.rule_180(self.tf_empty)
