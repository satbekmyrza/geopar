from geopar.triangulated_figure import TriangulatedFigure
from geopar.triangle import Triangle
from geopar.angle import Angle

__author__ = 'satbek'


class TFPreprocessor(object):
    """
    TFPreprocessor - Triangulated Figure Preprocessor
    encapsulates functions that deal with preprocessing a triangulated figure a_tf (look at methods' parameters).

    There are three theorems, by use of which we accomplish preprocessing:
    - Theorem 1: Rule of 180 degrees
    - Theorem 2: Rule of 360 degrees
    - Theorem 3: Pairing rule
    For more information on these rules, please refer to the paper.
    """

    @staticmethod
    def theorem_1(a_tf):
        """
        Completes unknown angles --where possible-- by using 180 degrees rule.
        """

        b = False
        for triangle in a_tf.get_triangles():
            b = triangle.complete_unknown_angle()
            if b and not a_tf.angles_deduced:
                # new information added
                a_tf.angles_deduced = True

    @staticmethod
    def theorem_2(a_tf):
        # Pre-processing method.
        # Checks all interior points if they have one missing angle around it.
        # Makes unknown angle known.

        interior_points = a_tf.get_interior_points()
        for point in interior_points:
            # counting unknown angles for a given interior point
            count_unknowns = 0
            for triangle in a_tf.triangles:
                if triangle.has_point(point):
                    if not triangle.angle_of_point(point).is_known():
                        count_unknowns += 1

            # if there is only 1 unknown, we can calculate it
            if count_unknowns == 1:

                # adding up all the angles and storing in sum_angles
                sum_angles = 0
                for triangle in a_tf.triangles:
                    if triangle.has_point(point):
                        sum_angles += triangle.angle_of_point(point)

                # finding the unknown angle
                unknown_angle = 360 - sum_angles

                # setting the unknown angle
                for triangle in a_tf.triangles:
                    if triangle.has_point(point):
                        if not triangle.angle_of_point(point).is_known():
                            # new information invoked
                            triangle.set_angle_by_index(triangle.get_points().index(point), unknown_angle)
                            if not a_tf.angles_deduced:
                                a_tf.angles_deduced = True

    @staticmethod
    def theorem_3(a_tf):
        # Precondition 1: a self has to have at least one interior point
        interior_points = a_tf.get_interior_points()

        # cycling through all interior points
        for point in interior_points:
            triangles = a_tf.triangles_with_point(point)

            set1, set2 = [], []
            triangles_with_unknown_angles = []
            count_unknown_angles = 0
            sum_angles = 0

            for _t in triangles:
                af = _t.angle_of_point(_t.point_following(point))
                ap = _t.angle_of_point(_t.point_preceding(point))

                if not af.is_known():
                    triangles_with_unknown_angles.append(_t)
                    count_unknown_angles += 1
                else:
                    set1.append(af)
                    sum_angles += af

                if not ap.is_known():
                    if af.is_known():
                        triangles_with_unknown_angles.append(_t)
                    count_unknown_angles += 1
                else:
                    set2.append(ap)
                    sum_angles += ap

            # collections.Counter is needed to check if two lists contain the same elements.
            # Lists may have repeated elements.
            from collections import Counter
            if Counter(set1) == Counter(set2) and count_unknown_angles == 2:
                sum_both = (len(triangles) - 2) * 180 - sum_angles
                unknown_angle = sum_both / 2
                for _t_ in triangles_with_unknown_angles:
                    for _tt_ in a_tf.triangles:
                        if _tt_.has_all_points(_t_.get_points()):
                            for _p in _t_.get_points():
                                if not _tt_.angle_of_point(_p).is_known() and _p != point:
                                    _tt_.set_angle_by_point(_p, unknown_angle)
                                    a_tf.angles_deduced = True
