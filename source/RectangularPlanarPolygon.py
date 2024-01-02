from TriangularPlanarPolygon import TriangularPlanarPolygon
from Point import Point
import numpy as np

class RectangularPlanarPolygon:
    """
    Represents a rectangular planar polygon, defined by two triangular faces.

    Attributes:
        vertices (list of Point): The four vertices defining the rectangle.
        triangle1 (TriangularPlanarPolygon): The first triangular part of the rectangle.
        triangle2 (TriangularPlanarPolygon): The second triangular part of the rectangle.
        normal (Vector): The normal vector of the rectangle's plane.
    """

    def __init__(self, vertices: list):
        """
        Initializes a RectangularPlanarPolygon with four specified vertices, creates two triangular faces, and calculates the normal.

        Args:
            vertices (list of Point): A list containing four Point objects representing the vertices of the rectangle.
        """
        if len(vertices) != 4:
            raise ValueError("A RectangularPlanarPolygon must be initialized with exactly four vertices.")

        self.vertices = vertices
        self.triangle1 = TriangularPlanarPolygon([vertices[0].copy(), vertices[1].copy(), vertices[2].copy()])
        self.triangle2 = TriangularPlanarPolygon([vertices[2].copy(), vertices[3].copy(), vertices[0].copy()])
        self.normal = self.triangle1.normal  # Using the normal from the first triangle

    def centroid(self) -> Point:
        """
        Calculates the centroid (middle point) of the rectangle.

        Returns:
            Point: The centroid of the rectangle.
        """
        x = (self.vertices[0].x + self.vertices[1].x + self.vertices[2].x + self.vertices[3].x) / 4
        y = (self.vertices[0].y + self.vertices[1].y + self.vertices[2].y + self.vertices[3].y) / 4
        z = (self.vertices[0].z + self.vertices[1].z + self.vertices[2].z + self.vertices[3].z) / 4
        return Point(x, y, z)

    def get_vertices(self):
        """
        Returns a list of all the vertices of the rectangular polygon.

        Returns:
            list: A list containing all the vertices of the rectangular polygon.
        """
        return self.vertices

    def random_point_inside(self):
        """
        Generates a random point inside the rectangular polygon.

        Returns:
            Point: A random point within the rectangle.
        """
        # Randomly choose one of the two triangles
        triangle = self.triangle1 if np.random.rand() < 0.5 else self.triangle2

        # Use the random point generator from TriangularPlanarPolygon
        return triangle.random_point_inside()
    
    def __str__(self) -> str:
        """
        Returns a string representation of the RectangularPlanarPolygon.

        Returns:
            str: The string representation of the RectangularPlanarPolygon.
        """
        vertex_coords = ', '.join(f"({v.x}, {v.y}, {v.z})" for v in self.vertices)
        normal_coords = f"({self.normal.x}, {self.normal.y}, {self.normal.z})"
        return f"RectangularPlanarPolygon(Vertices: [{vertex_coords}], Normal: {normal_coords})"
