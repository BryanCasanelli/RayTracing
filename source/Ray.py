from Point import Point
from Vector import Vector
from Material import Material
import numpy as np
import copy

class Ray:
    """
    Represents a ray in three-dimensional space.

    Attributes:
        origin (Point): The origin point of the ray.
        normal (Vector): The normal vector indicating the direction of the ray.
        wavelength (float): The wavelength of the ray.
        intensity (float): The intensity of the ray, ranging from 0.0 to 1.0.
        final_point (Point): The final point of the ray.
    """

    def __init__(self, origin: Point, normal: Vector, wavelength: float, intensity = 1.0) -> None:
        """
        Initializes the Ray instance with the specified origin, normal vector, and wavelength.

        Args:
            origin (Point): The origin point of the ray.
            normal (Vector): The normal vector indicating the direction of the ray.
            wavelength (float): The wavelength of the ray.
            intensity (float): The intensity of the ray, ranging from 0.0 to 1.0.
        """
        self.origin = origin
        self.normal = normal
        self.final_point = None
        self.wavelength = wavelength
        self.intensity = intensity
        self.medium = Material()
        self.used = False

    def __str__(self) -> str:
        """
        Returns a string representation of the Ray.

        Returns:
            str: The string representation of the Ray.
        """
        return (f"Ray(Origin: ({self.origin.x}, {self.origin.y}, {self.origin.z}), "
                f"Direction: ({self.normal.x}, {self.normal.y}, {self.normal.z}), "
                f"Wavelength: {self.wavelength})")
    
    def set_final_point(self, final_point: Point) -> None:
        """
        Sets the final point of the Ray.

        Args:
            final_point (Point): The final point of the Ray.
        """
        self.final_point = final_point
        distance = self.origin.distance(final_point)*10**-3  # Convert from mm to m
        n_img = self.medium.get_refractive_index(self.wavelength).imag
        alpha = 4*np.pi*n_img/(self.wavelength*10**-9)  # Convert from nm to m
        self.intensity *= np.exp(-alpha * distance)
    
    def wavelength_to_rgba(self):
        """
        Convert the wavelength in nanometers to an RGBA color using the CIE 1931 color space approximation.

        Returns:
            tuple: RGBA color represented as (R, G, B, Alpha) with values in the range [0, 1].
        """
        gamma = 0.8
        intensity_max = 255
        factor = 0.0
        R, G, B = 0, 0, 0

        if (self.wavelength >= 380) and (self.wavelength < 440):
            R = -(self.wavelength - 440) / (440 - 380)
            G = 0.0
            B = 1.0
        elif (self.wavelength >= 440) and (self.wavelength < 490):
            R = 0.0
            G = (self.wavelength - 440) / (490 - 440)
            B = 1.0
        elif (self.wavelength >= 490) and (self.wavelength < 510):
            R = 0.0
            G = 1.0
            B = -(self.wavelength - 510) / (510 - 490)
        elif (self.wavelength >= 510) and (self.wavelength < 580):
            R = (self.wavelength - 510) / (580 - 510)
            G = 1.0
            B = 0.0
        elif (self.wavelength >= 580) and (self.wavelength < 645):
            R = 1.0
            G = -(self.wavelength - 645) / (645 - 580)
            B = 0.0
        elif (self.wavelength >= 645) and (self.wavelength <= 750):
            R = 1.0
            G = 0.0
            B = 0.0

        # Adjust intensity
        if (self.wavelength >= 380) and (self.wavelength < 420):
            factor = 0.3 + 0.7 * (self.wavelength - 380) / (420 - 380)
        elif (self.wavelength >= 420) and (self.wavelength < 645):
            factor = 1.0
        elif (self.wavelength >= 645) and (self.wavelength <= 750):
            factor = 0.3 + 0.7 * (750 - self.wavelength) / (750 - 645)

        R = int(intensity_max * (R * factor) ** gamma)/255
        G = int(intensity_max * (G * factor) ** gamma)/255
        B = int(intensity_max * (B * factor) ** gamma)/255

        return (R, G, B, self.intensity)

    def copy(self):
        """
        Returns a copy of the Ray.

        Returns:
            Ray: A copy of the Ray.
        """
        return copy.deepcopy(self)