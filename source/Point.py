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
            x (float or list/tuple): The x-coordinate of the point or a list/tuple of [x, y, z].
            y (float, optional): The y-coordinate of the point. Not needed if x is a list/tuple.
            z (float, optional): The z-coordinate of the point. Not needed if x is a list/tuple.
        """
        if isinstance(x, (list, tuple)) and len(x) == 3:
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
        return Point(self.x, self.y, self.z)

    def get_coordinates(self) -> tuple:
        """
        Returns the coordinates of the point as a tuple.

        Returns:
            tuple: The point as a tuple (x, y, z).
        """
        return self.x, self.y, self.z


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