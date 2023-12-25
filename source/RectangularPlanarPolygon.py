from TriangularPlanarPolygon import TriangularPlanarPolygon
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
        self.triangle1 = TriangularPlanarPolygon([vertices[0], vertices[1], vertices[2]])
        self.triangle2 = TriangularPlanarPolygon([vertices[2], vertices[3], vertices[0]])
        self.normal = self.triangle1.normal  # Using the normal from the first triangle

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
