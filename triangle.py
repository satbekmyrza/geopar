__author__ = 'satbek'


from Geopar.angle import Angle


class Triangle:
    def __init__(self, three_points, three_angles):
        """
        INTENT:
        Define a triangle with 3 angles and 3 vertex points labeled by integers, in clockwise order.

        IMPORTANT:
        Vertices of a Triangle objects will be called 'points' throughout the program.

        PRE:
        (Distinct): three_points consists of distinct non-negative integers

        POST:
        self.points = three_points AND
        self.angles = three_angles

        NOTES:
        1. Raise an error if precondition (Distinct) is not met.

        ISSUES:
        1. find_third_angle method, returning True or False is a weak design.
           (Change detection mechanics)

        """

        self.points = three_points
        self.angles = three_angles

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

    def get_angles(self):
        """
        POST:
        self.angles is returned
        """

        return self.angles

    def get_points(self):
        """
        POST:
        self.points is returned
        """

        return self.points

    def angle_of_point(self, a_point):
        """
        INTENT:
        get the angle given a_point

        PRE:
        self.points contains a_point

        POST:
        angle of a_point is returned

        RAISES:
        ValueError, if self.points misses a_point

        NOTES:
        unittest should be implemented
        """

        if a_point not in self.points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        return self.angles[self.points.index(a_point)]

    def index_of_point(self, a_point):
        """
        INTENT:
        get the position of a_point in self.points

        PRE:
        self.points contains a_point

        POST:
        index is returned

        RAISES:
        ValueError, if self.points misses a_point

        NOTES:
        unittest should be implemented
        """
        if a_point not in self.points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        return self.get_points().index(a_point)

    def point_following(self, a_point):
        """
        INTENT:
        Returns a point that follows a_point in clockwise order.

        PRE:
        self.points contains a_point

        POST:
        a point following a_point is returned

        RAISES:
        ValueError, if self.points misses a_point

        NOTES:
        unittest should be implemented
        """

        if a_point not in self.points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        index_of_a_point = self.points.index(a_point)
        return self.points[(index_of_a_point + 1) % 3]

    def point_preceding(self, a_point):
        """
        INTENT:
        Returns a point that precedes a_point in clockwise order.

        PRE:
        self.points contains a_point

        POST:
        a point preceding a_point is returned

        RAISES:
        ValueError, if self.points misses a_point

        NOTES:
        unittest should be implemented
        """

        if a_point not in self.points:
            error_message = 'The point ({}) is not in a triangle!'
            raise ValueError(error_message.format(a_point))

        index_of_a_point = self.points.index(a_point)
        return self.points[(index_of_a_point - 1) % 3]

    def count_known(self):
        """
        INTENT:
        Count known angles in self

        POST:
        The number of known angles in self is returned

        NOTES:
        unittest should be implemented
        """

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
        a_point is in self.points

        POST:
        self.angle_of_point(a_point) == an_angle yields True

        RAISES:
        ValueError, if self.points misses a_point

        NOTES:
        unittest should be implemented
        """

        if a_point not in self.points:
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
        True is returned, if a_point is in self.points; False, otherwise

        NOTES:
        unittest should be implemented
        """

        return a_point in self.points

    def has_all_points(self, three_points):
        return set(self.points) == set(three_points)

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
        2. *True is returned, if change to triangle is made; False, otherwise.

        RAISES:
        None

        NOTES:
        * This is specifically done for the purposes in Geopar.triangulated_figure.TriangulatedFigure
        unittest should be implemented
        """

        if self.count_known() == 2:
            s = sum(self.angles).get_coefficients()
            third = Angle([-s[0], -s[1], 180-s[2]])
            for i in range(3):
                if not self.angles[i].is_known():
                    self.angles[i] = third

                    # change is made
                    return True

        # no change is made to self
        return False
