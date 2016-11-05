import unittest
from geopar.tfvalidator import TFValidator
from geopar.triangulated_figure import TriangulatedFigure

__author__ = 'satbek'


class TestTFValidator(unittest.TestCase):

    def setUp(self):
        self.validator = TFValidator()
        self.tf_empty = TriangulatedFigure()

    def test_rule_180(self):
        with self.assertRaises(Exception):
            self.validator.rule_180(self.tf_empty)
