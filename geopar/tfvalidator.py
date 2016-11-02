from geopar.triangulated_figure import TriangulatedFigure
from geopar.triangle import Triangle
from geopar.angle import Angle

__author__ = 'satbek'


class TFValidator(object):
    def __init(self):
        pass

    @staticmethod
    def rule_180_valid(a_tf):
        for t in a_tf.triangles:
            if sum(t.get_angles()) != t.get_angles()[0].get_angle_180():
                return False
        return True

    @staticmethod
    def rule_360_valid(a_tf):
        interior_points = a_tf.get_interior_points()
        for point in interior_points:
            _triangles = []
            for triangle in a_tf.triangles:
                if triangle.has_point(point):
                    _triangles.append(triangle)
            sum_angles = 0
            for triangle in _triangles:
                sum_angles += triangle.angle_of_point(point)
            if sum_angles != sum_angles.get_angle_360():
                return False
        return True

    @staticmethod
    def rule_pairing_valid(a_tf):
        set1, set2 = [], []
        from collections import Counter
        for point in a_tf.get_interior_points():
            for tri in a_tf.triangles_with_point(point):
                set1.append(tri.angle_of_point(tri.point_following(point)))
                set2.append(tri.angle_of_point(tri.point_preceding(point)))

            if Counter(set1) != Counter(set2):
                return False

        return True
