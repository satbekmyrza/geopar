from collections import Counter

__author__ = 'satbek'


class TFValidator(object):
    """
    TFValidator - Triangulated Figure Validator
    encapsulates functions that deal with validating a triangulated figure a_tf (look at methods' parameters).

    We conclude that a triangulated figure is valid when it passes all of the following three rules:
    1 - Rule of 180 degrees
    2 - Rule of 360 degrees
    3 - Pairing rule
    For more information on these rules, please refer to the paper.
    """

    @staticmethod
    def rule_180(a_tf):
        """
        Checks whether a rule of 180 degrees is valid in a triangulated figure a_tf.

        PRE
        a_tf is an instance of TriangulatedFigure class containing at least one triangle.

        POST
        True is returned if the rule is valid, False otherwise.
        """

        ########################################################################
        if a_tf.is_empty():
            raise Exception('a_tf is empty! See precondition PRE')
        ########################################################################

        for triangle_ in a_tf.get_triangles():
            if sum(triangle_.get_angles()) != 180:
                return False
        return True

    @staticmethod
    def rule_360(a_tf):
        """
        Checks whether a rule of 360 degrees is valid in a triangulated figure a_tf.

        PRE
        a_tf is an instance of TriangulatedFigure class containing at least one triangle.

        POST
        True is returned if the rule is valid, False otherwise.
        """

        ########################################################################
        if a_tf.is_empty():
            raise Exception('a_tf is empty! See precondition PRE')
        ########################################################################

        interior_points = a_tf.get_interior_points()

        for point in interior_points:
            _triangles = a_tf.triangles_with_point(point)

            sum_angles = 0
            for triangle in _triangles:
                sum_angles += triangle.angle_of_point(point)

            if sum_angles != 360:
                return False
        return True

    @staticmethod
    def rule_pairing(a_tf):
        set1, set2 = [], []
        for point in a_tf.get_interior_points():
            for tri in a_tf.triangles_with_point(point):
                set1.append(tri.angle_of_point(tri.point_following(point)))
                set2.append(tri.angle_of_point(tri.point_preceding(point)))

            if Counter(set1) != Counter(set2):
                return False

        return True

    @staticmethod
    def all_rules(a_tf):
        return TFValidator.rule_180(a_tf) and TFValidator.rule_360(a_tf) and TFValidator.rule_pairing(a_tf)
