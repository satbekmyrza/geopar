import unittest
from geopar.triangle import Triangle
from geopar.triangulated_figure import TriangulatedFigure

__author__ = 'ebraude'

# URL1: https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit?usp=sharing


class TestTriangulatedFigure(unittest.TestCase):

    def setUp(self):

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

        self.tf_empty = TriangulatedFigure()

    def test_constructor(self):

        t1 = Triangle([1, 2, 5], [20, 10, 150])
        t2 = Triangle([5, 2, 6], [80, 10, 90])
        t3 = Triangle([6, 2, 3], [140, 10, 30])
        t4 = Triangle([4, 6, 3], [80, 70, 30])
        t5 = Triangle([1, 4, 3], [20, 130, 30])
        t6 = Triangle([1, 5, 4], [20, 70, 90])
        t7 = Triangle([4, 5, 6], [60, 60, 60])
        tf1 = TriangulatedFigure([t1, t2, t3, t4, t5, t6, t7])
        print(tf1)

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

    def test_is_empty(self):
        self.assertTrue(self.tf_empty.is_empty())
        self.assertFalse(self.tf1.is_empty())



