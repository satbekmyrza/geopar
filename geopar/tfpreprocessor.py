from geopar.triangulated_figure import TriangulatedFigure
from geopar.triangle import Triangle
from geopar.angle import Angle
from collections import Counter

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

        for t in a_tf.get_triangles():
            t.complete_unknown_angle()

    @staticmethod
    def theorem_2(a_tf):
        """
        Computes unknown angle(s) at interior point(s) of a
        triangulated figure by using 360 degrees rule.
        For more information on 360 degrees rule, please refer to the paper.

        PRE1: a_tf is a triangulated figure with at least one interior point.
             len( a_tf.get_interior_points() ) > 0
        PRE2: Either any of interior points has exactly one unknown angle
              OR nothing is done
        POST: unknown angles are computed
        """

        def complete_unknown_angle(a_point):
            """
            Computes an unknown angle at a point by using 360 degrees rule.

            PRE1: a_point is an interior point of a triangulated figure a_tf
            PRE2: there is exactly one unknown angle at a_point
            POST: unknown angle (see PRE2) is computed
            """

            # (Counted) unknowns_count contains the number of unknown angles at a_point
            # unknowns_count is used to keep PRE1 true
            unknowns_count = a_tf.number_of_unknown_angles_at(a_point)

            # (Recorded) angle_points is a list of angle_points of the unknown_angle at a_point
            angle_points = None
            for triangle in a_tf.triangles_with_point(a_point):
                if not triangle.angle_of_point(a_point).is_known():
                    angle_points = triangle.get_angle_points_by_point(a_point)

            # (Summed up) angles_sum is a sum of known angles at a_point
            angles_sum = a_tf.sum_of_known_angles_at(a_point)

            # (Found and set) unknown_angle is the value of the unknown_angle
            unknown_angle = 360 - angles_sum
            if unknowns_count == 1:
                a_tf.set_angle_by_points(*angle_points, unknown_angle)

        for point in a_tf.get_interior_points():
            complete_unknown_angle(point)

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
