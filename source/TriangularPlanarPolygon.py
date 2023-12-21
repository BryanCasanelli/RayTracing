from Point import Point
from Vector import Vector
import numpy as np

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
        # Convert points to vectors
        v0 = Vector(self.vertices[0].x, self.vertices[0].y, self.vertices[0].z)
        v1 = Vector(self.vertices[1].x, self.vertices[1].y, self.vertices[1].z)
        v2 = Vector(self.vertices[2].x, self.vertices[2].y, self.vertices[2].z)

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
