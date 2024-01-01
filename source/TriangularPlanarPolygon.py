from Point import Point
from Vector import Vector
import numpy as np
from Ray import Ray

class TriangularPlanarPolygon:
    """
    Represents a triangular planar polygon in 3D space.

    Attributes:
        vertices (list of Point): The vertices of the triangle.
        normal (Vector): The normal vector of the plane in which the triangle lies.
    """

    def __init__(self, points: list):
        """
        Initializes a TriangularPlanarPolygon with three specified points.

        Args:
            points (list of Point): A list containing three Point objects representing the vertices of the triangle.

        Raises:
            ValueError: If the points do not form a valid triangle.
        """
        if len(points) != 3:
            raise ValueError("A TriangularPlanarPolygon must be initialized with exactly three points.")

        self.vertices = points
        self.normal = self._calculate_normal()

    def centroid(self) -> Point:
        """
        Calculates the centroid (middle point) of the triangle.

        Returns:
            Point: The centroid of the triangle.
        """
        x = (self.vertices[0].x + self.vertices[1].x + self.vertices[2].x) / 3
        y = (self.vertices[0].y + self.vertices[1].y + self.vertices[2].y) / 3
        z = (self.vertices[0].z + self.vertices[1].z + self.vertices[2].z) / 3
        return Point(x, y, z)

    def get_vertices(self) -> list:
        """
        Returns the vertices of the triangle as an array of Point objects.

        Returns:
            list: The vertices of the triangle.
        """
        return self.vertices

    def _calculate_normal(self) -> Vector:
        """
        Calculates the normal vector of the triangle's plane.

        Returns:
            Vector: The normal vector of the plane.
        """
        v0 = self.vertices[0]
        v1 = self.vertices[1]
        v2 = self.vertices[2]

        # Calculate the vectors representing two sides of the triangle
        edge1 = Vector(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
        edge2 = Vector(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)

        # Cross product of the two edges gives the normal
        normal = edge1.cross(edge2)
        normal.normalize()

        return normal
    
    def random_point_inside(self) -> Point:
        """
        Generates a random point inside the triangle.

        Returns:
            Point: A random point within the triangle.
        """
        # Generate two random numbers
        r1, r2 = np.random.rand(2)

        # Ensure the point lies inside the triangle
        if r1 + r2 > 1:
            r1, r2 = 1 - r1, 1 - r2

        # Vertices of the triangle
        p0, p1, p2 = self.vertices

        # Calculate the point using barycentric coordinates
        x = (1 - r1 - r2) * p0.x + r1 * p1.x + r2 * p2.x
        y = (1 - r1 - r2) * p0.y + r1 * p1.y + r2 * p2.y
        z = (1 - r1 - r2) * p0.z + r1 * p1.z + r2 * p2.z

        return Point(x, y, z)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the TriangularPlanarPolygon.

        Returns:
            str: The string representation of the TriangularPlanarPolygon.
        """
        vertex_coords = ', '.join(f"({v.x}, {v.y}, {v.z})" for v in self.vertices)
        normal_coords = f"({self.normal.x}, {self.normal.y}, {self.normal.z})"
        return f"TriangularPlanarPolygon(Vertices: [{vertex_coords}], Normal: {normal_coords})"
    
    def get_intersection(self, ray: Ray) -> Point:
        """
        Calculates the intersection point of the ray with the triangle.
        The equation being solved is: O + tD = P, where O is the ray origin, D is the direction vector,
        t is the scalar multiplier to find the point P on the ray that intersects the triangle's plane.

        Args:
            ray (Ray): The ray to calculate the intersection point with.

        Returns:
            Point: The intersection point of the ray with the triangle, or None if no intersection occurs.
            TriangularPlanarPolygon: The triangle that was intersected, or None if no intersection occurs.
        """
        # Convert the triangle's vertices and the ray's origin and direction to NumPy arrays
        V1 = self.vertices[0].get_coordinates()
        V2 = self.vertices[1].get_coordinates()
        V3 = self.vertices[2].get_coordinates()
        ray_origin = ray.origin.get_coordinates()
        ray_vector = ray.normal.get_coordinates()

        # Calculate the vectors representing the edges of the triangle
        edge1 = V2 - V1
        edge2 = V3 - V1

        # Calculate the vector perpendicular to both the ray direction and edge2 of the triangle
        h = np.cross(ray_vector, edge2)
        
        # Compute the dot product of edge1 and vector h; if it's near zero, ray is parallel to the triangle
        a = np.dot(edge1, h)
        if abs(a) < 1e-6:
            return None  # Ray is parallel to the triangle

        # Compute the inverse of 'a' for later calculations
        f = 1.0 / a

        # Calculate the vector from V1 to the ray origin
        s = ray_origin - V1

        # Compute the barycentric coordinate 'u'
        u = f * np.dot(s, h)
        # Check if 'u' is outside the triangle
        if u < 0.0 or u > 1.0:
            return None

        # Calculate vector perpendicular to vector 's' and edge1
        q = np.cross(s, edge1)

        # Compute the barycentric coordinate 'v'
        v = f * np.dot(ray_vector, q)
        # Check if 'v' is outside the triangle, or 'u+v' exceeds 1 (outside the triangle)
        if v < 0.0 or u + v > 1.0:
            return None

        # Compute the parameter 't' of the line equation that intersects the plane
        t = f * np.dot(edge2, q)
        
        # If t is positive, there is an intersection; otherwise, the ray goes away from the triangle
        if t > 1e-6:  # Intersection with the triangle
            # Calculate the actual intersection point
            intersection_point = ray_origin + ray_vector * t
            return Point(intersection_point[0], intersection_point[1], intersection_point[2])

        return None

