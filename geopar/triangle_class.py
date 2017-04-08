from geopar.angle_class import Angle


__author__ = 'satbek'


class Triangle:
    """
    --------------------------------------------------------------------------------------------------------------------
    Intent: Defines a triangle with 3 angles and 3 vertices (later called 'points'
    throughout the rest of the program), in clockwise order.

    --------------------------------------------------------------------------------------------------------------------
    Object attributes:
    _points contains three points (distinct int instances) in clockwise order.
    _angles contains corresponding three angles (Angle instances) in clockwise order.

    --------------------------------------------------------------------------------------------------------------------
    Class invariants:
    1. _points[i] corresponds to _angles[i] for i in [0, 2]
    2. _points contains three distinct non-negative int instances
    --------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, three_points, three_angles):
        """
        PRE1: three_points consists of three distinct non-negative integers
        PRE2: three_angles consists of three Angle|int|float instances

        NOTES:
        int and float angles in three_angles will be converted to Angle objects.
        """

        # convert int|float angles to Angle
        three_angles2 = []
        for angle in three_angles:
            if isinstance(angle, (int, float)):
                three_angles2.append(Angle([angle]))
            if isinstance(angle, Angle):
                three_angles2.append(angle)

        self._points = three_points
        self._angles = three_angles2

    def __str__(self):
        """
        Returns string representation of self.
        """

        return_string = 'TRIANGLE -> Vertices: {}, {}, {}; Angles: {}, {}, {}'.format(
            self.get_points()[0], self.get_points()[1], self.get_points()[2],
            self.get_angles()[0], self.get_angles()[1], self.get_angles()[2])

        return return_string

    def __hash__(self):
        """
        Computes and returns hash of self.
        """

        sorted_points = sorted(self._points)
        for_hash = str(sorted_points[0]) + str(hash(self.angle_of_point(sorted_points[0])))
        for_hash += str(sorted_points[1]) + str(hash(self.angle_of_point(sorted_points[1])))
        for_hash += str(sorted_points[2]) + str(hash(self.angle_of_point(sorted_points[2])))
        return hash(for_hash)

    def get_angles(self):
        """
        self._angles is returned
        """

        return self._angles

    def get_points(self):
        """
        self._points is returned
        """

        return self._points

    def angle_of_point(self, a_point):
        """
        INTENT: returns the angle of a_point
        PRE: self._points contains a_point
        POST: angle of a_point is returned
        """

        if a_point not in self._points:
            raise Exception('There is no such point.')

        return self._angles[self._points.index(a_point)]

    def index_of_point(self, a_point):
        """
        INTENT: returns the position of a_point in self._points
        PRE: self._points contains a_point
        POST: index is returned
        """

        if a_point not in self._points:
            raise Exception('There is no such point.')

        return self.get_points().index(a_point)

    def point_following(self, a_point):
        """
        INTENT: Returns a point that follows a_point in clockwise order.
        PRE: self._points contains a_point
        POST: a point following a_point is returned
        """

        if a_point not in self._points:
            raise Exception('There is no such point.')

        index_of_a_point = self._points.index(a_point)
        return self._points[(index_of_a_point + 1) % 3]

    def point_preceding(self, a_point):
        """
        INTENT: Returns a point that precedes a_point in clockwise order.
        PRE: self._points contains a_point
        POST: a point preceding a_point is returned
        """

        if a_point not in self._points:
            raise Exception('There is no such point.')

        index_of_a_point = self._points.index(a_point)
        return self._points[(index_of_a_point - 1) % 3]

    def count_known(self):
        """
        INTENT: Count known angles in self
        POST: The number of known angles in self is returned
        """

        count = 0
        for angle in self._angles:
            if angle.is_known():
                count += 1
        return count

    def has_point(self, a_point):
        """
        INTENT: Does self have a point a_point?
        POST: True is returned, if a_point is in self._points; False, otherwise
        """

        return a_point in self._points

    def has_all_points(self, three_points):
        return set(self._points) == set(three_points)

    def has_unknown_angle(self):
        """
        INTENT: Does self have unknown angles
        POST: True is returned, if self has an unknown angle; False, otherwise
        """

        return self.count_known() != 3

    def get_angle_points_by_point(self, a_point):
        ind = self.index_of_point(a_point)
        shift = (ind + 2) % 3
        points = self._points[shift:] + self._points[:shift]
        return points

    def set_angle_by_point(self, a_point, an_angle):
        """
        INTENT: Sets an angle of a_point in self to an_angle
        PRE: a_point is in self._points
        POST: self.angle_of_point(a_point) == an_angle
        """

        if a_point not in self._points:
            raise Exception('There is no such point.')

        self._angles[self.index_of_point(a_point)] = an_angle

    def set_angle_by_index(self, an_index, an_angle):
        """
        INTENT: Sets self._angles[an_index] in self to an_angle
        PRE: an_index is either 0, 1, or 2
        POST: self._angles[an_index] == an_angle
        """

        if an_index not in [0, 1, 2]:
            raise Exception('Bad index.')

        self._angles[an_index] = an_angle

    def sum_of_known_angles(self):
        """
        Computes the sum of known angles.
        """

        sum_ = 0
        for angle in self._angles:
            if angle.is_known():
                sum_ += angle

        return sum_

    def complete_unknown_angle(self):
        """
        Completes a triangle with one unknown angle.

        PRE: self.count_known() == 2 is True.
        POST: self.count_known() == 3 is True.
        """

        # Ensuring PRE
        if self.count_known() != 2:
            raise Exception('Something went wrong.')

        sum_ = self.sum_of_known_angles()
        third = 180 - sum_

        for i in range(3):
            if not self._angles[i].is_known():
                self._angles[i] = third
