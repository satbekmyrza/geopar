import unittest
from geopar.triangle import Triangle
from geopar.triangulated_figure import TriangulatedFigure

__author__ = 'ebraude'


class TestTriangulatedFigure(unittest.TestCase):

    def setUp(self):

        # TriangulatedFigure tf1 consists of seven Triangles t1-t7
        # Appearance: URL1 at the end

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

        # triangulated_figure0 consists of triangle0 and triangle1:
        # Appearance: URL1 at the end.

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

        print('test_get_points()')
        self.assertEqual(7, len(self.tf1.get_triangles()))  # 7 triangles
        self.assertEqual(6, len(self.tf1.get_points()))  # 6 points

    def test_triangles_with_vertex(self):

        print('test_triangles_with_point()')
        self.assertEqual(7, len(self.tf1.get_triangles()))  # 7 triangles

        # how can we check the order of triangles?

        triangles_ = self.tf1.triangles_with_point(4)
        self.assertEqual(4, len(triangles_))  # 4 triangles around point 4


        triangles_ = self.triangulated_figure1.triangles_with_point(26)
        self.assertEquals(3, len(triangles_))
        self.assertTrue(50 in triangles_[1].get_angles())
        triangles_ = self.triangulated_figure1.triangles_with_point(25)
        self.assertEquals(3, len(triangles_))
        triangles_ = self.triangulated_figure0.triangles_with_point(3)
        self.assertEquals(2, len(triangles_))
        self.assertTrue(130 in triangles_[1].get_angles())


# URL1: https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit?usp=sharing
