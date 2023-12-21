from TriangularPlanarPolygon import TriangularPlanarPolygon
import numpy as np

class RectangularPlanarPolygon:
    """
    Represents a rectangular planar polygon, defined by two triangular faces.

    Attributes:
        points (list of Point): The four points defining the rectangle.
        triangle1 (TriangularPlanarPolygon): The first triangular part of the rectangle.
        triangle2 (TriangularPlanarPolygon): The second triangular part of the rectangle.
        normal (Vector): The normal vector of the rectangle's plane.
    """

    def __init__(self, points: list):
        """
        Initializes a RectangularPlanarPolygon with four specified points, creates two triangular faces, and calculates the normal.

        Args:
            points (list of Point): A list containing four Point objects representing the vertices of the rectangle.
        """
        if len(points) != 4:
            raise ValueError("A RectangularPlanarPolygon must be initialized with exactly four points.")

        self.points = points
        self.triangle1 = TriangularPlanarPolygon([points[0], points[1], points[2]])
        self.triangle2 = TriangularPlanarPolygon([points[2], points[3], points[0]])
        self.normal = self.triangle1.normal  # Using the normal from the first triangle

    def get_vertices(self):
        """
        Returns a list of all the vertices of the rectangular polygon.

        Returns:
            list: A list containing all the vertices of the rectangular polygon.
        """
        return self.points

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
        point_coords = ', '.join(f"({p.x}, {p.y}, {p.z})" for p in self.points)
        normal_coords = f"({self.normal.x}, {self.normal.y}, {self.normal.z})"
        return f"RectangularPlanarPolygon(Points: [{point_coords}], Normal: {normal_coords})"