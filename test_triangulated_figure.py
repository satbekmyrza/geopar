import unittest
from Geopar.triangle import Triangle
from Geopar.triangulated_figure import TriangulatedFigure

__author__ = 'ebraude'


class TestTriangulatedFigure(unittest.TestCase):

    def setUp(self):

        # triangulated_figure0 consists of triangle0 and triangle1:
        # Appearance: URL1 at end
        self.triangle0 = Triangle([1, 3, 2], [30, 20, 130])
        self.triangle1 = Triangle([2, 3, 4], [25, 35, 120])
        self.triangulated_figure0 = TriangulatedFigure()
        self.triangulated_figure0.add(self.triangle0)
        self.triangulated_figure0.add(self.triangle1)

        self.triangle32 = Triangle([24, 26, 25], [50, 30, 100])  # surrounded by the 3 below
        self.triangle33 = Triangle([24, 25, 27], [30, 130, 20])
        self.triangle34 = Triangle([28, 25, 26], [30, 80, 70])
        self.triangle35 = Triangle([29, 26, 24], [30, 70, 80])
        self.triangulated_figure1 = TriangulatedFigure()
        self.triangulated_figure1.add(self.triangle32)
        self.triangulated_figure1.add(self.triangle33)
        self.triangulated_figure1.add(self.triangle34)
        self.triangulated_figure1.add(self.triangle35)

    def test_get_points(self):

        self.triangulated_figure0.to_string()
        self.assertEqual(2, len(self.triangulated_figure0.triangles))  # 2 triangles
        self.assertEqual(4, len(self.triangulated_figure0.get_points()))  # 4 get_points

        self.triangulated_figure1.to_string()
        self.assertEqual(4, len(self.triangulated_figure1.triangles))  # 4 triangles
        self.assertEqual(6, len(self.triangulated_figure1.get_points()))  # 6 get_points

    def test_triangles_with_vertex(self):

        triangles_ = self.triangulated_figure1.triangles_with_point(26)
        self.assertEquals(3, len(triangles_))
        self.assertTrue(50 in triangles_[1].get_angles())
        triangles_ = self.triangulated_figure1.triangles_with_point(25)
        self.assertEquals(3, len(triangles_))
        triangles_ = self.triangulated_figure0.triangles_with_point(3)
        self.assertEquals(2, len(triangles_))
        self.assertTrue(130 in triangles_[1].get_angles())

