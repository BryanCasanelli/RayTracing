import numpy as np
import copy

class Point:
    """
    Represents a point in three-dimensional space.

    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
        z (float): The z-coordinate of the point.
    """

    def __init__(self, x, y=None, z=None) -> None:
        """
        Initializes a new point with the specified x, y, and z coordinates.

        Args:
            x (float or np.ndarray or list/tuple): The x-coordinate of the point or a numpy array or a list/tuple of [x, y, z].
            y (float, optional): The y-coordinate of the point. Not needed if x is a numpy array or a list/tuple.
            z (float, optional): The z-coordinate of the point. Not needed if x is a numpy array or a list/tuple.
        """
        if isinstance(x, (list, tuple, np.ndarray)):
            if len(x) != 3:
                raise ValueError("Input must be a tuple, list, or numpy array of length 3")
            self.x, self.y, self.z = x
        else:
            self.x = x
            self.y = y
            self.z = z

    def copy(self):
        """
        Returns a copy of the Point.

        Returns:
            Point: A copy of the Point.
        """
        return copy.deepcopy(self)

    def get_coordinates(self) -> np.ndarray:
        """
        Returns the coordinates of the point as a numpy array.

        Returns:
            np.ndarray: The point as a numpy array [x, y, z].
        """
        return np.array([self.x, self.y, self.z])


    def __str__(self) -> str:
        """
        Returns a string representation of the Point.

        Returns:
            str: The string representation of the Point.
        """
        return f"Point(x={self.x}, y={self.y}, z={self.z})"
    
    def __eq__(self, other) -> bool:
        """
        Checks if this point is equal to another point.

        Args:
            other (Point): Another point to compare with.

        Returns:
            bool: True if both points are the same, False otherwise.
        """
        if not isinstance(other, Point):
            # Don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.z == other.z
    
    
    def distance(self, other) -> float:
        """
        Calculates the distance between this point and another point.

        Args:
            other (Point): Another point to calculate the distance to.

        Returns:
            float: The distance between the two points.
        """
        return np.linalg.norm(self.get_coordinates() - other.get_coordinates())