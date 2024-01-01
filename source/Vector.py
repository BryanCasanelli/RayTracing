import numpy as np
import warnings
import numpy as np
import copy

class Vector:
    """
    Represents a vector in three-dimensional space.

    Attributes:
        x (float): The x-component of the vector.
        y (float): The y-component of the vector.
        z (float): The z-component of the vector.
        module (float): The module (magnitude) of the vector.
    """

    def __init__(self, x: float, y: float = None, z: float = None) -> None:
        """
        Initializes a new Vector with the specified x, y, and z components and calculates its module.
        """
        if isinstance(x, (tuple, list, np.ndarray)):
            if len(x) != 3:
                raise ValueError("Input must be a tuple, list, or numpy array of length 3")
            self.x, self.y, self.z = x
        else:
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
        return np.linalg.norm(self.get_coordinates())

    def get_coordinates(self) -> tuple:
        """
        Returns a tuple containing the x, y, and z coordinates of the vector.

        Returns:
            tuple: A tuple containing the x, y, and z coordinates of the vector.
        """
        return np.array([self.x, self.y, self.z])

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
            self.module = self._calculate_module()

    def dot(self, other) -> float:
        """
        Calculates the dot product with another vector.

        Args:
            other (Vector): The other vector to calculate the dot product with.

        Returns:
            float: The dot product of the two vectors.
        """
        return np.dot(self.get_coordinates(), other.get_coordinates())

    def cross(self, other) -> 'Vector':
        """
        Calculates the cross product with another vector.

        Args:
            other (Vector): The other vector to calculate the cross product with.

        Returns:
            Vector: The cross product of the two vectors.
        """
        cross_product = np.cross(self.get_coordinates(), other.get_coordinates())
        return Vector(cross_product[0], cross_product[1], cross_product[2])

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
    
    def invert(self):
        """
        Inverts the vector.
        """
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
    
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
    
    def copy(self):
        """
        Returns a copy of the Vector.

        Returns:
            Vector: A copy of the Vector.
        """
        return copy.deepcopy(self)
