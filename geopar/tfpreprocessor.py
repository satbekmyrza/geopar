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
        Completes unknown angles --where possible-- by using 360 degrees rule.
        For more information, please refer to the paper.
        """

        """
        interior_points = a_tf.get_interior_points()
        for point in interior_points:

            # counting unknown angles for a given interior point
            sum_angles = 0
            tw_point = a_tf.triangles_with_point(point)
            count_unknowns = len(tw_point)
            for t in tw_point:
                if t.angle_of_point(point).is_known():
                    count_unknowns -= 1
                    sum_angles += t.angle_of_point(point)


            # for triangle in a_tf.triangles:
            #     if triangle.has_point(point):
            #         if not triangle.angle_of_point(point).is_known():
            #             count_unknowns += 1

            # if there is only 1 unknown, we can calculate it
            if count_unknowns == 1:

                # adding up all the angles and storing in sum_angles

                # sum_angles = 0
                # for triangle in a_tf.triangles:
                #     if triangle.has_point(point):
                #         sum_angles += triangle.angle_of_point(point)

                # finding the unknown angle
                unknown_angle = 360 - sum_angles

                # setting the unknown angle
                for triangle in a_tf.triangles:
                    if triangle.has_point(point):
                        if not triangle.angle_of_point(point).is_known():
                            # new information invoked
                            triangle.set_angle_by_index(triangle.get_points().index(point), unknown_angle)
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

                angle_following_list.append(angle_following)
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
