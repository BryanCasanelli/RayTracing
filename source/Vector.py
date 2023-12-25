import numpy as np
import warnings

class Vector:
    """
    Represents a vector in three-dimensional space.

    Attributes:
        x (float): The x-component of the vector.
        y (float): The y-component of the vector.
        z (float): The z-component of the vector.
        module (float): The module (magnitude) of the vector.
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Initializes a new Vector with the specified x, y, and z components and calculates its module.
        """
        self.x = x
        self.y = y
        self.z = z
        self.module = self._calculate_module()

    def _calculate_module(self) -> float:
        """
        Calculates the module (magnitude) of the vector.

        Returns:
            float: The module of the vector.
        """
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def get_coordinates(self) -> tuple:
        """
        Returns a tuple containing the x, y, and z coordinates of the vector.

        Returns:
            tuple: A tuple containing the x, y, and z coordinates of the vector.
        """
        return (self.x, self.y, self.z)

    def normalize(self):
        """
        Normalizes the vector (makes it a unit vector).
        If the vector is a zero vector, issues a warning and does not perform normalization.
        """
        mod = self.module
        if mod == 0:
            warnings.warn("Cannot normalize a zero vector. The vector remains unchanged.", RuntimeWarning)
        else:
            self.x /= mod
            self.y /= mod
            self.z /= mod

    def dot(self, other) -> float:
        """
        Calculates the dot product with another vector.

        Args:
            other (Vector): The other vector to calculate the dot product with.

        Returns:
            float: The dot product of the two vectors.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other) -> 'Vector':
        """
        Calculates the cross product with another vector.

        Args:
            other (Vector): The other vector to calculate the cross product with.

        Returns:
            Vector: The cross product of the two vectors.
        """
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def angle_with(self, other) -> float:
        """
        Calculates the angle between this vector and another vector.

        Args:
            other (Vector): The other vector to calculate the angle with.

        Returns:
            float: The angle in radians between the two vectors.
        """
        dot_product = self.dot(other)
        magnitude_product = self.module * other.module
        if magnitude_product == 0:
            raise ValueError("Cannot calculate angle with a zero vector")
        return np.arccos(dot_product / magnitude_product)
    
    @staticmethod
    def random_unit_vector():
        """
        Generates a random unit vector.

        Returns:
            Vector: A random unit vector.
        """
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.random.uniform(0, np.pi)
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)
        return Vector(x, y, z)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the Vector.

        Returns:
            str: The string representation of the Vector.
        """
        return f"Vector(x={self.x}, y={self.y}, z={self.z}, module={self.module})"
