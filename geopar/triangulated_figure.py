from geopar.angle import Angle

__author__ = 'mostly satbek'


class TriangulatedFigure:

    # Class Invariant 1: Every triangle in self.triangles has
    # a unique set of vertices

    # Class Invariant 2: Every Triangle in self.triangles shares two get_points with another
    # !!!

    def __init__(self, triangles=None):
        # the Triangle objects that make up self

        if triangles:
            self._triangles = triangles
        else:
            self._triangles = []

    def get_state(self):
        # !!!
        return hash(str(sorted(list(map(hash, self._triangles)))))

    def add(self, a_triangle):
        # Precondition 1: a_triangle is a Triangle instance
        # Precondition 2: len(self.triangles) < 2
        #   --XOR--
        #   a_triangle ... is not in self.triangles AND
        #   ... shares two vertices with a Triangle in old(self.triangles)
        # Postcondition: a_triangle is in self.triangles

        self._triangles.append(a_triangle)

    def set_angle_by_angle_points(self, p1, p2, p3, angle_):
        """
        Set an angle in self to angle_.
        The angle is defined by three points p1, p2, and p3. In other words, the angle is
        an angle of point p2 in triangle with points p1, p2, and p3.

        PRE
        Points are given in clockwise order.
        """

        for triangle in self._triangles:
            if triangle.has_all_points([p1, p2, p3]):
                triangle.set_angle_by_point(p2, angle_)

    def get_angle_by_points(self, p1, p2, p3):
        """
        PRE
        Points are given in clockwise order.
        """

        for triangle in self._triangles:
            if triangle.has_all_points([p1, p2, p3]):
                return triangle.angle_of_point(p2)

    def get_triangles(self):
        return self._triangles

    def get_points(self):
        """
        Returns union of all points from self.triangles
        Postcondition: all points returned.
        """

        all_points = list()
        for triangle in self._triangles:
            all_points.extend(triangle.get_points())
        return list(set(all_points))

    def __str__(self):
        return_str = ""
        for current_triangle in self._triangles:
            return_str += str(current_triangle)
            return_str += "\n"
        return return_str

    def all_angles_known(self):
        for t in self._triangles:
            if t.has_unknown():
                return False
        return True

    def is_empty(self):
        return not bool(self._triangles)

    def triangles_with_point(self, a_point):
        # Precondition: At least one triangle in self.triangles contains a_point
        # Returns the (contiguous) list of self.triangles containing a_point
        # in clockwise order

        # [Collected]: triangles_with_a_point =
        # the triangles in self.triangles containing a_point [Note 3]

        triangles_with_a_point = []
        for triangle in self._triangles:
            if triangle.has_point(a_point):
                triangles_with_a_point.append(triangle)

        # (In Order): triangles_in_order is a non-empty sub-list of
        # triangles_with_a_point, which is in clockwise order
        # AND triangles_remaining = triangles_with_a_point\triangles_in_order
        # [Note 2]

        triangles_in_order = [triangles_with_a_point[0]]
        triangles_remaining = triangles_with_a_point[1:]

        while len(triangles_in_order) < len(triangles_with_a_point):
            for triangle_ in triangles_remaining:
                point_following = triangles_in_order[0].point_following(a_point)
                if triangle_.point_preceding(a_point) == point_following:
                    triangles_in_order.insert(0, triangle_)
                    triangles_remaining.remove(triangle_)
                    break
                point_preceding = triangles_in_order[-1].point_preceding(a_point)
                if triangle_.point_following(a_point) == point_preceding:
                    triangles_in_order.append(triangle_)
                    triangles_remaining.remove(triangle_)
                    break

        # (Complement): len(triangles_in_order) = len(triangles_with_a_point)
        return triangles_in_order

    def get_interior_points(self):
        """
        INTENT:
        Find all interior points of self (TriangulatedFigure)

        POST:
        interior_points is returned

        OBJECTIVES:
         (Found 1a): found the points that have more than 2 triangles attached to them
                     AND
         (Found 1b): saved them in point_nums, alongside with number of triangles that they are in
         (Found 2): found interior points
         (Complement): returned interior_points

        """

        # (Found 1a)
        all_points = self.get_points()
        point_nums = []
        for point in all_points:
            n = len(self.triangles_with_point(point))
            if n > 2:
                # (Found 1b)
                point_nums.append((point, n))

        # (Found 2)
        interior_points = []
        for point_num in point_nums:
            points = []
            for triangle in self.get_triangles():
                if triangle.has_point(point_num[0]):
                    points.extend(triangle.get_points())

            if len(set(points)) == point_num[1] + 1:
                interior_points.append(point_num[0])

        # (Complement): all interior points found
        return interior_points

    def number_of_unknown_angles_at(self, a_point):
        """
        Returns the number of unknown angles at a_point.

        PRE: a_point is in self.get_points

        POST: count contains the number of unknown angles at a_point
        """

        count = 0
        triangles = self.triangles_with_point(a_point)
        for triangle in triangles:
            angle = triangle.angle_of_point(a_point)
            if not angle.is_known():
                count += 1
        return count

    def sum_of_known_angles_at(self, a_point):
        """
        Returns the sum of known angles at a_point.

        PRE: a_point is in self.get_points

        POST: sum_angles contains the sum of known angles at a_point
        """

        sum_angles = 0
        triangles = self.triangles_with_point(a_point)
        for triangle in triangles:
            angle = triangle.angle_of_point(a_point)
            if angle.is_known():
                sum_angles += angle

        return sum_angles

    def angle_points_of_unknown_angles_at(self, a_point):
        """
        Returns a list of angle points of unknown angles at a_point.

        PRE: a_point is in self.get_points

        POST: list_of_points contains angle points of unknown angles
        """

        list_of_points = []
        triangles = self.triangles_with_point(a_point)
        for triangle in triangles:
            angle = triangle.angle_of_point(a_point)
            if not angle.is_known():
                angle_points = triangle.get_angle_points_by_point(a_point)
                list_of_points.append(angle_points)

        return list_of_points

    def complete_unknown_angle_at(self, a_point):
        """
        Computes an unknown angle at a point by using 360 degrees rule.

        PRE1: a_point is an interior point of a triangulated figure a_tf
        PRE2: there is exactly one unknown angle at a_point
        POST: unknown angle (see PRE2) is computed
        """

        # (Counted) unknowns_count contains the number of unknown angles at a_point
        # unknowns_count is used to keep PRE1 true
        unknowns_count = self.number_of_unknown_angles_at(a_point)

        # (Recorded) angle_points is a list of angle_points of unknown_angle at a_point
        angle_points = self.angle_points_of_unknown_angles_at(a_point)[-1]

        # (Summed up) angles_sum is a sum of known angles at a_point
        angles_sum = self.sum_of_known_angles_at(a_point)

        # (Found and set) unknown_angle is the value of the unknown_angle
        unknown_angle = 360 - angles_sum
        if unknowns_count == 1:
            self.set_angle_by_angle_points(*angle_points, unknown_angle)