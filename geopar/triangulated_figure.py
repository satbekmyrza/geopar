from geopar.angle import Angle

__author__ = 'mostly satbek'


class TriangulatedFigure:

    # Class Invariant 1: Every triangle in self.triangles has
    # a unique set of vertices

    # Class Invariant 2: Every Triangle in self.triangles shares two get_points with another

    def __init__(self, triangles_=None):
        # the Triangle objects that make up self

        if triangles_:
            self.triangles = triangles_
        else:
            self.triangles = []

        self.angles_deduced = False

    def get_state(self):
        return hash(str(sorted(list(map(hash, self.triangles)))))

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

        all_points = list()
        for triangle in self.triangles:
            all_points.extend(triangle.get_points())
        return list(set(all_points))

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

    def is_empty(self):
        return not bool(self.triangles)

    def triangles_with_point(self, a_point):
        # Precondition: At least one triangle in self.triangles contains a_point
        # Returns the (contiguous) list of self.triangles containing a_point
        # in clockwise order

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
