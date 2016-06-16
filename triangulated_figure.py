__author__ = 'mostly satbek'


from Geopar.triangle import Triangle
from Geopar.anglenew import Angle


class TriangulatedFigure:

    # Class Invariant 1: Every triangle in self.triangles has
    # a unique set of vertices

    # Class Invariant 2: Every Triangle in self.triangles shares two get_points with another

    def __init__(self):
        # the Triangle objects that make up self

        self.triangles = []
        self.anything_new = False

    def add(self, a_triangle):
        # Precondition 1: a_triangle is a Triangle instance
        # Precondition 2: len(self.triangles) < 2
        #   --XOR--
        #   a_triangle ... is not in self.triangles AND
        #   ... shares two vertices with a Triangle in old(self.triangles)
        # Postcondition: a_triangle is in self.triangles

        self.triangles.append(a_triangle)

    def get_triangles(self):
        return self.triangles

    def get_points(self):
        """
        Returns union of all points from self.triangles
        Postcondition: all points returned.
        """

        all_points = set()
        for triangle in self.triangles:
            for point in triangle.get_points():
                all_points.add(point)
        return list(all_points)

    def __str__(self):
        return_str = ""
        for current_triangle in self.triangles:
            return_str += str(current_triangle)
            return_str += "\n"
        return return_str

    def all_angles_known(self):
        for t in self.triangles:
            if t.has_unknown():
                return False
        return True

    def rule_180_valid(self):
        for t in self.triangles:
            if sum(t.get_angles()) != t.get_angles()[0].get_angle_180():
                return False
        return True

    def rule_360_valid(self):
        interior_points = self.get_interior_points()
        for point in interior_points:
            _triangles = []
            for triangle in self.triangles:
                if triangle.has_point(point):
                    _triangles.append(triangle)
            sum_angles = 0
            for triangle in _triangles:
                sum_angles += triangle.angle_of_point(point)
            if sum_angles != sum_angles.get_angle_360():
                return False
        return True

    def rule_pairing_valid(self):
        set1, set2 = [], []
        from collections import Counter
        for point in self.get_interior_points():
            for tri in self.triangles_with_point(point):
                set1.append(tri.angle_of_point(tri.point_following(point)))
                set2.append(tri.angle_of_point(tri.point_preceding(point)))

            if Counter(set1) != Counter(set2):
                return False

        return True

    def triangles_with_point(self, a_point):
        # Precondition: At least one triangle in self.triangles contains a_point
        # Returns the (contiguous) list of self.triangles containing a_point
        # in clockwise order
        # Example: URL1 (see at end)

        # [Collected]: triangles_with_a_point =
        # the triangles in self.triangles containing a_point [Note 3]

        triangles_with_a_point = []
        for triangle in self.triangles:
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

    def preprocess_theorem_1(self):
        # Pre-processing method.
        # Checks for triangles with one unknown angle, makes the angles known.

        b = False
        for triangle in self.get_triangles():
            b = triangle.complete_unknown_angle()
            if b and not self.anything_new:
                # new information added
                self.anything_new = True

    def preprocess_theorem_2(self):
        # Pre-processing method.
        # Checks all interior points if they have one missing angle around it.
        # Makes unknown angle known.

        interior_points = self.get_interior_points()
        b = False
        for point in interior_points:
            # counting unknown angles for a given interior point
            count_unknowns = 0
            for triangle in self.triangles:
                if triangle.has_point(point):
                    if not triangle.angle_of_point(point).is_known():
                        count_unknowns += 1

            # if there is only 1 unknown, we can calculate it
            if count_unknowns == 1:

                # adding up all the angles and storing in sum_angles
                sum_angles = Angle([0,0,0])
                for triangle in self.triangles:
                    if triangle.has_point(point):
                        sum_angles += triangle.angle_of_point(point)
                sum_angles = sum_angles.get_coefficients()

                # finding the unknown angle
                unknown_angle = Angle([-sum_angles[0], -sum_angles[1], 360-sum_angles[2]])

                # setting the unknown angle
                for triangle in self.triangles:
                    if triangle.has_point(point):
                        if not triangle.angle_of_point(point).is_known():
                            # new information invoked
                            triangle.set_angle_by_index(triangle.get_points().index(point), unknown_angle)
                            if b and not self.anything_new:
                                self.anything_new = True

    def preprocess_theorem_3_pairing(self):
        # Precondition 1: a self has to have at least one interior point
        interior_points = self.get_interior_points()

        # cycling through all interior points
        for point in interior_points:
            triangles = self.triangles_with_point(point)

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
                unknown_angle = sum_both // 2
                for _t_ in triangles_with_unknown_angles:
                    for _tt_ in self.triangles:
                        if _tt_.has_all_points(_t_.get_points()):
                            for _p in _t_.get_points():
                                if not _tt_.angle_of_point(_p).is_known() and _p != point:
                                    _tt_.set_angle_by_point(_p, unknown_angle)
                                    self.anything_new = True
