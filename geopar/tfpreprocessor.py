from geopar.triangulated_figure import TriangulatedFigure
from geopar.triangle import Triangle
from geopar.angle import Angle
from collections import Counter

__author__ = 'satbek'


class TFPreprocessor(object):
    """
    TFPreprocessor (Triangulated Figure Preprocessor) - encapsulates preprocessing functions.

    Each function is an implementation of a theorem. There are three theorems:
    - Theorem 1: 180-degree rule;
    - Theorem 2: 360-degree rule;
    - Theorem 3: Pairing rule.

    For more information on these theorems, please refer to the paper.
    """

    @staticmethod
    def theorem_1(a_tf):
        """
        Implementation of 180-degree rule.

        Completes unknown angles of triangles in a_tf by 180-degree rule.

        PRE: isinstance(a_tf, TriangulatedFigure) is True.
        POST: !!!
        """

        for triangle in a_tf.get_triangles():
            triangle.complete_unknown_angle()

    @staticmethod
    def theorem_2(a_tf):
        """
        Implementation of 360-degree rule.

        Completes unknown angles of triangles in a_tf by 360-degree rule.

        PRE1: isinstance(a_tf, TriangulatedFigure) is True.
        PRE2: EITHER
                  len( a_tf.get_interior_points() ) > 0
                  AND
                  there is exactly one unknown angle at any of a_tf.get_interior_points()
              OR
                  nothing is done

        POST: !!!
        """

        for point in a_tf.get_interior_points():
            a_tf.complete_unknown_angle_at(point)

    @staticmethod
    def theorem_2b(a_tf):
        """
        Completes unknown angles --where possible-- by using 360 degrees rule.
        For more information, please refer to the paper.
        """

        for point in a_tf.get_interior_points():
            # get all triangles with given interior point
            triangles = a_tf.triangles_with_point(point)

            # count unknown angles around interior point
            unknowns_count = 0
            # sum known angles around interior point
            sum_angles = 0
            # angle points of all angles around interior point
            angle_points = []
            # record angle points of latest unknown angle
            points_of_unknown_angle = None

            # get all angle points of angles around interior point
            for t in triangles:
                angle_points.append(t.get_angle_points_by_point(point))

            # cycle through angle points (is equivalent to cycling through angles) around interior point
            for angle_point in angle_points:
                # get the angle
                angle = a_tf.get_angle_by_points(*angle_point)

                # restore control variables
                if not angle.is_known():
                    unknowns_count += 1
                    points_of_unknown_angle = angle_point
                else:
                    sum_angles += angle

            # record result of computation
            if unknowns_count == 1:
                a_tf.set_angle_by_points(*points_of_unknown_angle, 360 - sum_angles)

    @staticmethod
    def theorem_3(a_tf):
        # traversing through interior points
        for point in a_tf.get_interior_points():

            # triangles around interior point
            triangles = a_tf.triangles_with_point(point)

            angle_following_list = []
            angle_preceding_list = []

            unknown_following_count = 0
            unknown_preceding_count = 0
            sum_angles = 0

            points_of_unknown_angles = []

            # traverse through triangles around interior point
            for t in triangles:
                point_following = t.point_following(point)
                point_preceding = t.point_preceding(point)

                angle_following = t.angle_of_point(point_following)
                angle_preceding = t.angle_of_point(point_preceding)

                if angle_following.is_known():
                    angle_following_list.append(angle_following)
                if angle_preceding.is_known():
                    angle_preceding_list.append(angle_preceding)

                if not angle_following.is_known():
                    unknown_following_count += 1
                    points_of_unknown_angles.append(t.get_angle_points_by_point(point_following))
                else:
                    sum_angles += angle_following

                if not angle_preceding.is_known():
                    unknown_preceding_count += 1
                    points_of_unknown_angles.append(t.get_angle_points_by_point(point_preceding))
                else:
                    sum_angles += angle_preceding

            if unknown_following_count == 1 and unknown_following_count == 1 and \
                    Counter(angle_following_list) == Counter(angle_preceding_list):
                angle_to_set = ((len(triangles) - 2) * 180 - sum_angles) / 2
                a_tf.set_angle_by_points(*points_of_unknown_angles[0], angle_to_set)
                a_tf.set_angle_by_points(*points_of_unknown_angles[1], angle_to_set)
