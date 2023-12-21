from Point import Point
from Ray import Ray
from Vector import Vector
from RectangularPlanarPolygon import RectangularPlanarPolygon
import numpy as np

class RaySource:
    """
    A class to generate rays either from a specific point or from a RectangularPlanarPolygon,
    with both modes using a given direction and aperture angle.

    Attributes:
        origin (Point): The origin point for the ray (used for point mode).
        normal (Vector): The normal vector indicating the direction of the ray.
        aperture_angle (float): The aperture angle in radians, used for defining the spread of the ray.
        rectangle (RectangularPlanarPolygon): The rectangular area from which to generate rays (used for rectangle mode).
        min_wavelength (float): The minimum wavelength for the ray.
        max_wavelength (float): The maximum wavelength for the ray.
        mode (str): Mode of ray generation ('point' or 'rectangle').
        intensity (float): The intensity of the ray.
    """

    def __init__(self, origin: Point, normal: Vector, aperture_angle_grades: float, min_wavelength=380, max_wavelength=740, rectangle=None, mode='rectangle', intensity = 1.0):
        """
        Initializes the RaySource with specified parameters.

        Args:
            origin (Point): The origin point of the ray (for point mode).
            normal (Vector): The normal vector indicating the direction of the ray.
            aperture_angle_grades (float): The aperture angle in grades (converted to radians).
            min_wavelength (float): The minimum wavelength, default is 380 nm.
            max_wavelength (float): The maximum wavelength, default is 740 nm.
            rectangle (RectangularPlanarPolygon, optional): The rectangular area for ray generation (for rectangle mode).
            mode (str, optional): The mode of ray generation ('point' or 'rectangle'), default is 'point'.
            intensity (float): The intensity of the ray.
        """
        self.origin = origin
        self.normal = normal
        self.aperture_angle = np.radians(aperture_angle_grades)  # Convert grades to radians
        self.min_wavelength = min_wavelength
        self.max_wavelength = max_wavelength
        self.rectangle = rectangle
        self.mode = mode if rectangle else 'point'
        self.intensity = intensity

    def _random_vector_in_cone(self) -> Vector:
        """
        Generates a random vector within a cone defined by a normal vector and an aperture angle.

        Returns:
            Vector: A random vector within the specified cone.
        """
        if self.aperture_angle == 0:
            return Vector(self.normal.x, self.normal.y, self.normal.z)
        while True:
            random_vector = Vector.random_unit_vector()
            angle = random_vector.angle_with(self.normal)

            if angle <= self.aperture_angle:
                return random_vector
        

    def _random_point_in_rectangle(self):
        """
        Generates a random point inside the RectangularPlanarPolygon.

        Returns:
            Point: A random point within the rectangle.
        """
        # Use the random point generator from RectangularPlanarPolygon
        return self.rectangle.random_point_inside()

    def _random_wavelength(self):
        """
        Generates a random wavelength within the specified range.

        Returns:
            float: The wavelength.
        """
        return np.random.uniform(self.min_wavelength, self.max_wavelength)

    def get_next_ray(self):
        """
        Generates the next ray based on the initial configuration.

        Returns:
            Ray: The generated ray with random direction and wavelength.
        """
        wavelength = self._random_wavelength()
        direction = self._random_vector_in_cone()

        if self.mode == 'point':
            origin = self.origin
        elif self.mode == 'rectangle':
            origin = self._random_point_in_rectangle()

        return Ray(origin, direction, wavelength,intensity = self.intensity)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the RaySource.

        Returns:
            str: The string representation of the RaySource.
        """
        origin_str = f"Origin: ({self.origin.x}, {self.origin.y}, {self.origin.z})"
        normal_str = f"Normal: ({self.normal.x}, {self.normal.y}, {self.normal.z})"
        mode_str = f"Mode: {self.mode}"
        aperture_angle_str = f"Aperture Angle: {self.aperture_angle} radians"
        wavelength_range_str = f"Wavelength Range: {self.min_wavelength}-{self.max_wavelength} nm"

        return f"RaySource({origin_str}, {normal_str}, {mode_str}, {aperture_angle_str}, {wavelength_range_str})"