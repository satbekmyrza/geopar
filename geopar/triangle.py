from geopar.angle import Angle

"""
ISSUES:

SUGGESTIONS:

NOTES:

"""

__author__ = 'satbek'


class Triangle:
    """
    INTENT:
    Defines a triangle with 3 angles and 3 vertices labeled by integers, in clockwise order.

    NOTES:
    Triangle vertices will be called 'points' throughout the rest of the program.

    _points contains three points (int instances) in clockwise order.
    _angles contains corresponding three angles (Angle instances) in clockwise order.
    """

    def __init__(self, three_points, three_angles):
        """
        PRE1: three_points consists of three distinct non-negative integers
        PRE2: three_angles consists of three Angle|int|float instances

        NOTES:
        int and float angles in three_angles will be converted to Angle objects.
        """

        # PRE1
        # non-negative
        if not all(list(map(lambda x: x > 0, three_points))):
            raise Exception('Negative point provided.')
        # exactly 3 distinct
        if len(three_points) != 3:
            raise Exception('Wrong number of points provided.')
        elif len(set(three_points)) != 3:
            raise Exception('Wrong number of points provided.')

        # PRE2
        for angle in three_angles:
            if not isinstance(angle, (Angle, int, float)):
                raise Exception('Angle provided is not Angle|int|float.')

        # convert int|float angles to Angle
        three_angles2 = []
        for angle in three_angles:
            if isinstance(angle, (int, float)):
                three_angles2.append(Angle([angle]))
            if isinstance(angle, Angle):
                three_angles2.append(angle)

        self._points = three_points
        self.angles = three_angles2

    def __str__(self):
        """
        INTENT:
        Make self printable

        POST:
        String representation of self is returned
        """
        return_string = 'Triangle: Vertices {}, {}, {}; Angles {}, {}, {}'.format(
            self.get_points()[0], self.get_points()[1], self.get_points()[2],
            self.get_angles()[0], self.get_angles()[1], self.get_angles()[2])

        return return_string

    def __hash__(self):
        """
        Computes hash of self.
        """

        sorted_points = sorted(self._points)
        for_hash = str(sorted_points[0]) + str(hash(self.angle_of_point(sorted_points[0])))
        for_hash += str(sorted_points[1]) + str(hash(self.angle_of_point(sorted_points[1])))
        for_hash += str(sorted_points[2]) + str(hash(self.angle_of_point(sorted_points[2])))
        return hash(for_hash)

    def get_angles(self):
        """
        POST:
        self.angles is returned
        """

        return self.angles

    def get_angle_points_by_point(self, a_point):
        ind = self.index_of_point(a_point)
        shift = (ind + 2) % 3
        points = self._points[shift:] + self._points[:shift]
        return points

    def get_points(self):
        """
        POST:
        self._points is returned
        """

        return self._points

    def angle_of_point(self, a_point):
        """
        INTENT:
        get the angle given a_point

        PRE:
        self._points contains a_point

        POST:
        angle of a_point is returned

        RAISES:
        ValueError, if self._points misses a_point

        NOTES:
        unittest should be implemented
        """

        if a_point not in self._points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        return self.angles[self._points.index(a_point)]

    def index_of_point(self, a_point):
        """
        INTENT:
        get the position of a_point in self._points

        PRE:
        self._points contains a_point

        POST:
        index is returned

        RAISES:
        ValueError, if self._points misses a_point

        NOTES:
        unittest should be implemented
        """
        if a_point not in self._points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        return self.get_points().index(a_point)

    def point_following(self, a_point):
        """
        INTENT:
        Returns a point that follows a_point in clockwise order.

        PRE:
        self._points contains a_point

        POST:
        a point following a_point is returned

        RAISES:
        ValueError, if self._points misses a_point

        NOTES:
        unittest should be implemented
        """

        if a_point not in self._points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        index_of_a_point = self._points.index(a_point)
        return self._points[(index_of_a_point + 1) % 3]

    def point_preceding(self, a_point):
        """
        INTENT:
        Returns a point that precedes a_point in clockwise order.

        PRE:
        self._points contains a_point

        POST:
        a point preceding a_point is returned

        RAISES:
        ValueError, if self._points misses a_point

        NOTES:
        unittest should be implemented
        """

        if a_point not in self._points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        index_of_a_point = self._points.index(a_point)
        return self._points[(index_of_a_point - 1) % 3]

    def count_known(self):
        """
        INTENT:
        Count known angles in self

        POST:
        The number of known angles in self is returned

        NOTES:
        unittest should be implemented
        """

        if isinstance(self.angles[0], int) and isinstance(self.angles[1], int) and isinstance(self.angles[2], int):
            return 3

        count = 0
        for angle in self.angles:
            if angle.is_known():
                count += 1
        return count

    def set_angle_by_point(self, a_point, an_angle):
        """
        INTENT:
        Setting an angle of a_point in self to an_angle

        PRE:
        a_point is in self._points

        POST:
        self.angle_of_point(a_point) == an_angle yields True

        RAISES:
        ValueError, if self._points misses a_point

        NOTES:
        unittest should be implemented
        """

        if a_point not in self._points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        self.angles[self.index_of_point(a_point)] = an_angle

    def set_angle_by_index(self, an_index, an_angle):
        """
        INTENT:
        Setting self.angles[an_index] in self to an_angle

        PRE:
        an_index is either 0, 1, or 2

        POST:
        self.angles[an_index] == an_angle yields True

        RAISES:
        ValueError, if an_index is not in [0, 1, 2]

        NOTES:
        unittest should be implemented
        """

        if an_index not in [0, 1, 2]:
            error_message = 'The index ({}) is bad!'
            raise ValueError(error_message.format(an_index))

        self.angles[an_index] = an_angle

    def has_point(self, a_point):
        """
        INTENT:
        Learning if self has a point a_point

        POST:
        True is returned, if a_point is in self._points; False, otherwise

        NOTES:
        unittest should be implemented
        """

        return a_point in self._points

    def has_all_points(self, three_points):
        return set(self._points) == set(three_points)

    def has_unknown(self):
        """
        INTENT:
        Learning if self has unknown angles

        POST:
        True is returned, if self has an unknown angle; False, otherwise

        NOTES:
        unittest should be implemented
        """

        return self.count_known() != 3

    def complete_unknown_angle(self):
        """
        INTENT:
        If self has an unknown angle, this method completes it using 180 rule.

        PRE:
        Two angles in self.angles are known, and one is unknown

        POST:
        1. All three angles in self.angles are known
        """

        if self.count_known() == 2:
            s = 0
            for an in self.get_angles():
                if an.is_known():
                    s += an
            # s = sum(self.angles).get_coefficients()
            s = s.get_coefficients()
            third = 180 - Angle(s)
            for i in range(3):
                if not self.angles[i].is_known():
                    self.angles[i] = third
